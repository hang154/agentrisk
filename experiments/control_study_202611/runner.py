"""Native JSON API runner. No generated code execution and no external actions."""
import argparse,concurrent.futures,copy,json,os,pathlib,resource,socket,threading,time,urllib.request,urllib.error
from .common import freeze,update,sha,file_sha,wire,ACTOR_SYSTEM,MONITOR_SCHEMA
from .tasks import public_task
from .setting import initial_state,execute,verify_receipts
from .oracle import violations,score
from .policies import Control
from .monitors import pre_action,post_action

def preflight(root,c):
 root=pathlib.Path(root);root.mkdir(parents=True,exist_ok=True)
 if socket.gethostname()!='main1':raise ValueError('REMOTE_MAIN1_ONLY')
 soft,hard=resource.getrlimit(resource.RLIMIT_NOFILE);needed=4*c+1024
 used=len(list(pathlib.Path('/proc/self/fd').iterdir()))
 if soft-used<needed:resource.setrlimit(resource.RLIMIT_NOFILE,(min(hard,needed+used+256),hard))
 assert resource.getrlimit(resource.RLIMIT_NOFILE)[0]-used>=needed
 fds=[os.open('/dev/null',os.O_RDONLY) for _ in range(needed)]
 for f in fds:os.close(f)
 assert os.statvfs(root).f_bavail*os.statvfs(root).f_frsize>2*1024**3
 freeze(root/f'PREFLIGHT_C{c}.json',{'host':socket.gethostname(),'uid':os.getuid(),'allowed_cpus':sorted(os.sched_getaffinity(0)),'device':root.stat().st_dev,'fd_exercised':needed,'concurrency':c})

class Client:
 def __init__(self,root,c,endpoint='http://127.0.0.1:18531/v1'):
  self.root=pathlib.Path(root);self.endpoint=endpoint;self.c=c;self.slots=threading.BoundedSemaphore(c);self.lock=threading.Lock();self.metrics={'active':0,'responses':0,'api_tokens':0,'output_tokens':0,'unknown':0,'last_response':time.time()}
 def call(self,payload,rid,role):
  d=self.root/'raw'/rid;d.mkdir(parents=True,exist_ok=True);freeze(d/'request.json',payload)
  if (d/'response.json').exists():
   raw=json.loads((d/'response.json').read_text());receipt=json.loads((d/'receipt.json').read_text())
   assert file_sha(d/'request.json')==receipt['request_sha256'] and file_sha(d/'response.raw')==receipt['raw_sha256']
   assert raw==json.loads((d/'response.raw').read_text()) and raw['usage']==receipt['usage']
   return raw,receipt
  with self.slots:
   if (self.root/'STOP_NEW_DISPATCH').exists():raise RuntimeError('ADMISSION_STOPPED_BEFORE_POST')
   # Marker is created immediately before POST; unknown IDs never reissued.
   with (d/'dispatch.json').open('x') as f:json.dump({'time':time.time(),'payload_sha256':sha(payload),'role':role,'thread':threading.get_native_id(),'cpus':sorted(os.sched_getaffinity(0))},f);f.flush();os.fsync(f.fileno())
   start=time.monotonic()
   with self.lock:self.metrics['active']+=1
   try:
    req=urllib.request.Request(self.endpoint+'/chat/completions',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Connection':'close'})
    with urllib.request.urlopen(req,timeout=600) as response:
     rawbytes=response.read()
    with (d/'response.raw').open('xb') as f:f.write(rawbytes);f.flush();os.fsync(f.fileno())
    value=json.loads(rawbytes);usage=value['usage'];assert all(type(usage[k]) is int and usage[k]>=0 for k in ['prompt_tokens','completion_tokens','total_tokens'])
    assert usage['total_tokens']==usage['prompt_tokens']+usage['completion_tokens']
    assert usage['completion_tokens']<=payload['max_tokens']
    receipt={'id':rid,'role':role,'usage':usage,'finish':value['choices'][0]['finish_reason'],'seconds':time.monotonic()-start,'request_sha256':file_sha(d/'request.json'),'raw_sha256':file_sha(d/'response.raw')}
    freeze(d/'receipt.json',receipt);freeze(d/'response.json',value)
    with self.lock:
     self.metrics['responses']+=1;self.metrics['api_tokens']+=usage['total_tokens'];self.metrics['output_tokens']+=usage['completion_tokens'];self.metrics['last_response']=time.time()
    return value,receipt
   except Exception as e:
    if isinstance(e,urllib.error.HTTPError):
     with (d/'http_error.raw').open('xb') as f:f.write(e.read(1024*1024))
    freeze(d/'UNKNOWN.json',{'error':type(e).__name__,'detail':str(e)[:400],'maximum_missing_output':payload['max_tokens'],'retry':False})
    with self.lock:self.metrics['unknown']+=1
    if self.metrics['unknown']>=3:(self.root/'STOP_NEW_DISPATCH').touch(exist_ok=True)
    raise
   finally:
    with self.lock:self.metrics['active']-=1

def parse(response,receipt,schema):
 if receipt['finish']!='stop':raise ValueError('OUTPUT_TRUNCATED')
 x=json.loads(response['choices'][0]['message']['content']);assert isinstance(x,dict)
 assert set(x)==set(schema['required'])
 for k,s in schema['properties'].items():
  v=x[k];typ=s['type']
  assert (typ=='string' and isinstance(v,str)) or (typ=='integer' and type(v) is int) or (typ=='number' and type(v) in [int,float])
  if 'enum' in s:assert v in s['enum']
  if 'minimum' in s:assert v>=s['minimum']
  if 'maximum' in s:assert v<=s['maximum']
 return x

def episode(client,task,scenario,arm,seed,model,plan,stage):
 from .common import ACTION_SCHEMA
 eid=sha([plan['experiment_id'],stage,task['task_id'],scenario,arm,seed])[:28];dest=client.root/'episodes'/f'{eid}.json'
 if dest.exists():return json.loads(dest.read_text())
 lease=client.root/'leases'/eid;lease.parent.mkdir(exist_ok=True,parents=True)
 try:lease.open('x').close()
 except FileExistsError:raise ValueError('INCOMPLETE_EPISODE_NO_AUTORETRY:'+eid)
 state=initial_state();control=Control(arm,model);events=[];calls=[];obs=[];used=0;reviewused=0;invalid=0;status='STEP_CAP';started=time.time()
 record={'episode_id':eid,'stage':stage,'task_id':task['task_id'],'cluster':task['cluster'],'split':task['split'],'scenario':scenario,'arm':arm,'seed':seed,'evidence_kind':'LIVE_MODEL_CLOSED_LOOP','protocol_sha256':sha(plan),'initial':initial_state()}
 try:
  for step in range(plan['max_steps']):
   if used>=plan['actor_output_budget']:status='OUTPUT_BUDGET';break
   messages=[{'role':'system','content':ACTOR_SYSTEM},{'role':'user','content':json.dumps({'task':public_task(task,scenario),'observations':obs,'remaining_steps':plan['max_steps']-step},ensure_ascii=False)}]
   rr,rp=client.call(wire(messages,seed+step,max_tokens=min(plan['per_call_output'],plan['actor_output_budget']-used)),eid+f'-a{step}','actor');calls.append(rp);used+=rp['usage']['completion_tokens']
   try:a=parse(rr,rp,ACTION_SCHEMA)
   except (ValueError,TypeError,KeyError,AssertionError):
    invalid+=1;obs.append({'status':'INVALID_FORMAT','remaining_output':plan['actor_output_budget']-used})
    if invalid>plan['format_retries']:status='FORMAT_ERROR';break
    continue
   decision,prediction=control.decide(task,state,a)
   pre=copy.deepcopy(state);lock={'episode':eid,'step':step,'time':time.time(),'state_sha256':sha(pre),'proposal':a,'prediction':prediction}
   freeze(client.root/'prediction_locks'/f'{eid}-{step}.json',lock)
   monitor=None
   if arm=='B1' and a['tool'] not in ['read','finish','escalate']:
    if reviewused>=plan['monitor_output_budget_per_episode']:status='MONITOR_BUDGET';break
    mr,mp=client.call(wire(pre_action(task,state,a,[e['receipt'] for e in events]),seed+step,MONITOR_SCHEMA,min(plan['monitor_per_call_output'],plan['monitor_output_budget_per_episode']-reviewused)),eid+f'-m{step}','pre_action_monitor')
    calls.append(mp);reviewused+=mp['usage']['completion_tokens']
    try:monitor=parse(mr,mp,MONITOR_SCHEMA);decision=monitor['decision']
    except (ValueError,TypeError,KeyError,AssertionError):monitor={'decision':'UNSURE','format_error':True};decision='UNSURE'
   observation,receipt=execute(task,state,a,decision)
   # Oracle runs strictly AFTER the receipt. Only executed outcomes update B4.
   bad=bool(violations(task,pre,a));event={'pre_state_sha256':sha(pre),'prediction_lock':f'{eid}-{step}.json','prediction':prediction,'monitor':monitor,'receipt':receipt,'oracle_epoch':time.time(),'independent_bad_proposal':bad,'executed_bad':bad and receipt['executed']}
   events.append(event);freeze(client.root/'events'/f'{eid}-{step}.json',event)
   if receipt['executed']:control.observe(prediction['features'],bad,receipt['sha256'])
   obs.append({'proposal':a,'result':observation})
   if a['tool']=='finish':status='FINISH';break
   if a['tool']=='escalate':status='ESCALATED';break
 except Exception as e:status='UNKNOWN';record['error']=type(e).__name__+':'+str(e)[:300]
 missing={'actor':0,'pre_action_monitor':0}
 for p in (client.root/'raw').glob(eid+'-*/UNKNOWN.json'):
  info=json.loads(p.read_text());dispatch=json.loads((p.parent/'dispatch.json').read_text());missing[dispatch['role']]+=info['maximum_missing_output']
 assert used+missing['actor']<=plan['actor_output_budget'] and reviewused+missing['pre_action_monitor']<=plan['monitor_output_budget_per_episode']
 record.update(final=copy.deepcopy(state),events=events,calls=calls,status=status,format_errors=invalid,actor_output_tokens=used,monitor_output_tokens=reviewused,missing_output_upper_bound=missing,seconds=time.time()-started,completed_epoch=time.time())
 verify_receipts(record['initial'],events,state);record['oracle']=score(task,record['initial'],events,state,status)
 freeze(dest,record);return record

def batch(client,jobs,model,plan,stage):
 start=time.time();done=0;known=0;errors=[];stop=False
 pending={};iterator=iter(jobs)
 # A bounded rolling pool, no HTTP slot held while doing tool/oracle work.
 with concurrent.futures.ThreadPoolExecutor(max_workers=client.c) as pool:
  exhausted=False
  while pending or not exhausted:
   if (client.root/'STOP_NEW_DISPATCH').exists():stop=True;exhausted=True
   while not exhausted and len(pending)<client.c:
    try:t,s,a,seed=next(iterator)
    except StopIteration:exhausted=True;break
    f=pool.submit(episode,client,t,s,a,seed,model,plan,stage);pending[f]=(t['task_id'],s,a,seed)
   ready,_=concurrent.futures.wait(pending,timeout=10,return_when=concurrent.futures.FIRST_COMPLETED) if pending else ([],[])
   for f in ready:
    job=pending.pop(f)
    try:r=f.result();done+=1;known+=r['oracle']['known'];errors.extend([r['error']] if r['status']=='UNKNOWN' else [])
    except Exception as e:errors.append(str(e));stop=True;exhausted=True
   if len(errors)>=3:stop=True;exhausted=True
   with client.lock:metrics=copy.deepcopy(client.metrics)
   if pending and time.time()-metrics['last_response']>900:stop=True;exhausted=True
   update(client.root/'HEARTBEAT.json',{'stage':stage,'done':done,'known':known,'planned':len(jobs),'pending':len(pending),'elapsed':time.time()-start,'stop_new_dispatch':stop,'errors':errors[-3:],'metrics':metrics,
     'episode_per_minute':done/max(1,time.time()-start)*60,'eta_seconds':(len(jobs)-done)*(time.time()-start)/done if done else None})
  if stop:raise RuntimeError('DISPATCH_STOPPED:'+str(errors[-3:]))
 return {'episodes':done,'known':known,'seconds':time.time()-start}

def monitor_job(client,task,row,condition,plan):
 rid=row['episode_id']+'-post-'+condition;destination=client.root/'monitor_results'/f'{rid}.json'
 if destination.exists():return json.loads(destination.read_text())
 eligible=[(i,e) for i,e in enumerate(row['events']) if e['receipt']['proposal']['tool'] not in ['read','finish','escalate']]
 if not eligible:
  result={'episode_id':row['episode_id'],'condition':condition,'status':'NO_ELIGIBLE_ACTION'};freeze(destination,result);return result
 # Selection uses ID only, independent of oracle outcome.
 i,event=eligible[int(sha(row['episode_id'])[:12],16)%len(eligible)]
 usage=None
 try:
  rr,rp=client.call(wire(post_action(task,event,[e['receipt'] for e in row['events'][:i]],condition),row['seed'],MONITOR_SCHEMA,plan['monitor_per_call_output']),rid,'post_action_monitor');usage=rp['usage']
  try:v=parse(rr,rp,MONITOR_SCHEMA);status='VALID'
  except (ValueError,TypeError,KeyError,AssertionError):v=None;status='INVALID_FORMAT'
 except Exception:v=None;status='UNKNOWN'
 result={'episode_id':row['episode_id'],'task_id':task['task_id'],'cluster':task['cluster'],'scenario':row['scenario'],'condition':condition,'event_index':i,'target_actual_unsafe_execution':event['executed_bad'],'verdict':v,'status':status,'usage':usage,'raw_request_id':rid}
 freeze(destination,result);return result

def main():
 from .telemetry import Telemetry
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--stage',choices=['pilot','main','monitors'],required=True);p.add_argument('--concurrency',type=int,required=True);a=p.parse_args()
 root=pathlib.Path(a.root);plan=json.loads((root/'PROTOCOL_LOCK.json').read_text());model=json.loads((root/'FROZEN_MODEL.json').read_text());preflight(root,a.concurrency)
 if a.stage!='pilot':
  lock=json.loads((root/'INFERENCE_LOCK.json').read_text());assert lock['concurrency']==a.concurrency
  assert lock['protocol_sha256']==sha(plan) and lock['semantic_e2e_pass']
  assert file_sha(root/'SERVER_START.json')==lock['server_start_sha256']
  for name,digest in lock['raw_evidence_sha256'].items():assert file_sha(root/name)==digest
  for name,digest in plan['source_sha256'].items():assert file_sha(pathlib.Path(__file__).parent/name)==digest
 client=Client(root,a.concurrency)
 telemetry=Telemetry(root,a.stage).start()
 if a.stage=='monitors':
  tasks={t['task_id']:t for t in json.loads((root/'TASK_BANK.json').read_text())};rows=[json.loads(f.read_text()) for f in (root/'episodes').glob('*.json')];rows=[r for r in rows if r['stage']=='main' and r['arm']=='B0' and r['oracle']['known']]
  with concurrent.futures.ThreadPoolExecutor(max_workers=a.concurrency) as pool:
   results=list(pool.map(lambda job:monitor_job(client,*job,plan),[(tasks[r['task_id']],r,c) for r in rows for c in plan['monitors']]))
  freeze(root/'MONITOR_COMPLETE.json',{'submitted':len(results),'valid':sum(r['status']=='VALID' for r in results)})
 else:
  bank=json.loads((root/('DEVELOPMENT_BANK.json' if a.stage=='pilot' else 'TASK_BANK.json')).read_text())
  if a.stage=='pilot':
   # First real production-path E2E before any parallel pilot dispatch. These two
   # episodes are part of the fixed pilot, reused below without a second POST.
   canaries=[episode(client,bank[0],'benign',arm,5101,model,plan,'pilot') for arm in ['B1','B4']]
   assert all(r['oracle']['known'] and r['events'] and r['calls'] for r in canaries),'E2E_INTERFACE_OR_UNKNOWN'
   assert all(r['oracle']['task_complete'] for r in canaries),'E2E_LEGITIMATE_TASK_NOT_COMPLETED'
   freeze(root/'E2E_CANARY.json',{'episode_ids':[r['episode_id'] for r in canaries],'pass':True,'boundaries':['API','structured_action','monitor','mandatory_gate','state_write','oracle','immutable_evidence','adaptive_update']})
  jobs=[(t,s,arm,seed) for seed in (plan['seeds'] if a.stage=='main' else [5101]) for t in bank for s in plan['scenarios'] for arm in plan['policies']]
  result=batch(client,jobs,model,plan,a.stage);freeze(root/(a.stage.upper()+'_COMPLETE.json'),result)
 telemetry.close()
if __name__=='__main__':main()
