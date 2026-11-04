import argparse,concurrent.futures,copy,json,os,pathlib,time,shutil
from experiments.control_study_202611.common import freeze,update,sha,file_sha,wire,MONITOR_SCHEMA
from experiments.control_study_202611.runner import Client,parse,preflight
from experiments.control_study_202611.monitors import post_action

CONDITIONS=['M0','M1','M2','M3','M2_PROSE']
def prepare(root,old):
 root=pathlib.Path(root);old=pathlib.Path(old)
 rows=[json.loads(p.read_text()) for p in sorted((old/'episodes').glob('*.json'))]
 rows=[r for r in rows if r['stage']=='main' and r['arm']=='B0']
 jobs=[{'episode_id':r['episode_id'],'event_index':i,'condition':c} for r in rows for i,e in enumerate(r['events']) if e['receipt']['proposal']['tool'] not in ['read','finish','escalate'] for c in CONDITIONS]
 plan={'track':'retrospective_v1_monitor_census','jobs':len(jobs),'source_main_episodes':len(rows),'new_independent_population':False,'source_protocol_sha256':file_sha(old/'PROTOCOL_LOCK.json'),'source_sha256':file_sha(__file__),'model':'openai/gpt-oss-20b','max_tokens':4096,'reasoning_effort':'medium','concurrency':512,'no_unknown_retry':True}
 freeze(root/'CENSUS_PROTOCOL_LOCK.json',plan);freeze(root/'CENSUS_QUEUE.json',jobs)
 return plan,jobs,rows

def run(root,old):
 root=pathlib.Path(root);old=pathlib.Path(old);plan,jobs,rows=prepare(root,old)
 allowed=os.sched_getaffinity(0);cpus=allowed&set(range(36,48,2));assert cpus;os.sched_setaffinity(0,cpus)
 preflight(root,512);assert json.loads((old/'INFERENCE_LOCK.json').read_text())['actual_http_semaphore']==512
 tasks={t['task_id']:t for t in json.loads((old/'TASK_BANK.json').read_text())};rows={r['episode_id']:r for r in rows};client=Client(root,512)
 def one(j):
  rid=j['episode_id']+'-event'+str(j['event_index'])+'-'+j['condition'];dest=root/'census_results'/f'{rid}.json'
  if dest.exists():return json.loads(dest.read_text())
  row=rows[j['episode_id']];i=j['event_index'];e=row['events'][i];oldpath=old/'monitor_results'/(row['episode_id']+'-post-'+j['condition']+'.json')
  prior=json.loads(oldpath.read_text()) if oldpath.exists() else None
  result=dict(j,task_id=row['task_id'],cluster=row['cluster'],seed=row['seed'],target_actual_unsafe_execution=e['executed_bad'])
  if prior and prior.get('event_index')==i:
   result.update(origin='REUSED_V1',status=prior['status'],verdict=prior['verdict'],usage=prior['usage'],raw_request_id=prior['raw_request_id'],source_result_sha256=file_sha(oldpath));shutil.copytree(old/'raw'/prior['raw_request_id'],root/'raw'/prior['raw_request_id'],dirs_exist_ok=True)
  else:
   payload=wire(post_action(tasks[row['task_id']],e,[x['receipt'] for x in row['events'][:i]],j['condition']),row['seed'],MONITOR_SCHEMA,4096)
   try:
    rr,rp=client.call(payload,rid,'post_action_monitor_census')
    try:v=parse(rr,rp,MONITOR_SCHEMA);status='VALID'
    except (ValueError,AssertionError,KeyError,TypeError):v=None;status='INVALID_FORMAT'
    result.update(origin='NEW_MODEL_CALL',status=status,verdict=v,usage=rp['usage'],raw_request_id=rid)
   except Exception as ex:result.update(origin='NEW_MODEL_CALL',status='UNKNOWN',verdict=None,usage=None,error=type(ex).__name__,raw_request_id=rid)
  freeze(dest,result);return result
 # First genuinely new call is the production-path canary, not an extra replay.
 first=next(j for j in jobs if json.loads((old/'monitor_results'/(j['episode_id']+'-post-'+j['condition']+'.json')).read_text()).get('event_index')!=j['event_index'])
 canary=one(first);assert canary['status']=='VALID';freeze(root/'CENSUS_CANARY.json',canary)
 start=time.time();done=new=unknown=0
 with concurrent.futures.ThreadPoolExecutor(max_workers=512) as pool:
  for r in pool.map(one,jobs):
   done+=1;new+=r['origin']=='NEW_MODEL_CALL';unknown+=r['status']=='UNKNOWN'
   if done%25==0:update(root/'CENSUS_HEARTBEAT.json',{'time':time.time(),'done':done,'planned':len(jobs),'new':new,'unknown':unknown,'seconds':time.time()-start,'api':client.metrics})
 freeze(root/'CENSUS_COMPLETE.json',{'rows':done,'new_rows':new,'reused_rows':done-new,'unknown':unknown,'seconds':time.time()-start,'api':client.metrics})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--old',required=True);p.add_argument('--prepare',action='store_true');a=p.parse_args()
 if a.prepare:prepare(a.root,a.old)
 else:run(a.root,a.old)
