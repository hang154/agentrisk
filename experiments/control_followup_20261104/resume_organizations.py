"""Continue only never-POSTed work. Original partial rows and unknown calls stay frozen."""
import collections,concurrent.futures,copy,json,os,pathlib,shutil,time
from .organization import Team
from experiments.control_study_202611.runner import Client,preflight
from experiments.control_study_202611.common import sha,file_sha,freeze,update

def reconstruct(old,new,r,task,prior,attack,rawdirs):
 team=Team(r['job'],task,prior,attack,new);team.state=copy.deepcopy(r['final']);team.events=copy.deepcopy(r['events']);team.calls=copy.deepcopy(r['calls']);team.used=r['output_tokens'];team.missing=0;team.unknown=False
 by_agent={a:[] for a in range(r['job']['agents'])}
 for e in r['events']:by_agent[e['agent']].append(e)
 for a,events in by_agent.items():
  if events:
   e=events[-1];d=old/'raw'/e['request_id'];q=json.loads((d/'request.json').read_text());rr=json.loads((d/'response.json').read_text())
   team.messages[a]=q['messages'][1:]+[{'role':'assistant','content':rr['choices'][0]['message']['content']},{'role':'user','content':json.dumps({'decision':e['decision'],'executed':e['executed'],'receipt_sha256':e['receipt_sha256']})}]
   if e['action']['tool']=='finish':team.active.discard(a)
  # A prior invalid action removed this actor; do not silently add it back.
  cs=[c for c in r['calls'] if c['id'].endswith('-a'+str(a))]
  if cs:
   last=max(cs,key=lambda c:int(c['id'].rsplit('-r',1)[1].split('-a')[0]))
   if not any(e['request_id']==last['id'] for e in events):team.active.discard(a)
 pending=[]
 for d in rawdirs:
  p=d/'request.json'
  if (d/'dispatch.json').exists():continue
  assert not (d/'response.raw').exists() and not (d/'UNKNOWN.json').exists()
  q=json.loads(p.read_text());rid=d.name;roundno,a=map(int,rid.rsplit('-r',1)[1].split('-a'));s=0 if r['job']['sessions']=='single' else roundno;pending.append((roundno,a,s,rid,q));team.active.add(a)
 assert pending and len({x[0] for x in pending})==1;team.round=pending[0][0];team.expected={a for _,a,_,_,_ in pending};team.responses={};team.reserved=sum(q['max_tokens'] for _,_,_,_,q in pending)
 assert r['missing_output_upper_bound']==team.reserved,'Only release escrow proven never dispatched'
 works=[(team,a,s,rid,q,q['messages'],q['max_tokens']) for _,a,s,rid,q in sorted(pending)]
 return team,works

def run(old,root):
 old,root=pathlib.Path(old),pathlib.Path(root);root.mkdir(exist_ok=True,parents=True);assert old.stat().st_dev==root.stat().st_dev;load=lambda p:json.loads(p.read_text());os.sched_setaffinity(0,os.sched_getaffinity(0)&set(range(36,48,2)));preflight(root,512)
 for name in ['TASK_BANK.json','ORG_QUEUE.json','ORG_PROTOCOL_LOCK.json','FROZEN_MODEL.json','ATTACK_LOCK.json','ORG_CANARY.json']:
  if not (root/name).exists():os.link(old/name,root/name)
 for name in ['raw','prediction_locks','pre_action_inputs']:
  shutil.copytree(old/name,root/name,copy_function=os.link,dirs_exist_ok=True)
 tasks={t['task_id']:t for t in load(root/'TASK_BANK.json')};prior=load(root/'FROZEN_MODEL.json');attack=load(root/'ATTACK_LOCK.json')['selected_note'];rows=[load(p) for p in sorted((old/'teams').glob('*.json'))];queue=collections.deque();done=0;mapping=[];actual_unknowns=[]
 rawindex=collections.defaultdict(list)
 for d in (old/'raw').iterdir():rawindex[d.name.split('-r')[0]].append(d)
 for r in rows:
  p=old/'teams'/f'{r["id"]}.json';unknowns=[d/'UNKNOWN.json' for d in rawindex[r['id']] if (d/'UNKNOWN.json').exists()]
  if r['status']=='COMPLETE' or unknowns:
   freeze(root/'teams'/p.name,r);done+=r['job']['seed']!=7000;actual_unknowns.extend(str(x.relative_to(old)) for x in unknowns);continue
  assert r['job']['seed']!=7000
  team,works=reconstruct(old,root,r,tasks[r['task_id']],prior,attack,rawindex[r['id']]);queue.extend(works);mapping.append(dict(id=r['id'],original_result_sha256=file_sha(p),never_posted_request_ids=[w[3] for w in works],original_completed_calls=len(r['calls']),original_missing_upper_released=r['missing_output_upper_bound'],original_round=team.round))
 freeze(root/'CONTINUATION_LOCK.json',{'original_root':old.name,'actual_unknown_requests_never_reissued':actual_unknowns,'resumed_teams':len(mapping),'reused_complete_or_actual_unknown_main_teams':done,'runtime':'scoped Harmony trailing-terminal parser repair; generation unchanged','commit_order_amendment':'Within a partially committed round, previously unposted agents commit after preserved earlier commits. No original state transitions are rolled back.','source_sha256':file_sha(__file__),'mapping':mapping})
 client=Client(root,512);pending={};start=time.time()
 def call(w):
  assert not (old/'raw'/w[3]/'dispatch.json').exists(),'NO_REDISPATCH_OF_OLD_REQUEST'
  try:rr,rp=client.call(w[4],w[3],'organization_actor');return rr,rp,None
  except Exception as e:return None,None,type(e).__name__
 with concurrent.futures.ThreadPoolExecutor(max_workers=512) as pool:
  while queue or pending:
   while queue and len(pending)<512:
    w=queue.popleft();pending[pool.submit(call,w)]=w
   finished,_=concurrent.futures.wait(pending,timeout=5,return_when=concurrent.futures.FIRST_COMPLETED)
   for f in finished:
    w=pending.pop(f);t=w[0];t.accept(w,f.result())
    if t.expected<=t.responses.keys():
     t.advance();ws=t.ready()
     if ws:queue.extend(ws)
     else:t.finish();done+=1
   update(root/'ORG_HEARTBEAT.json',{'time':time.time(),'done':done,'planned':1728,'inflight':len(pending),'ready_calls':len(queue),'seconds':time.time()-start,'api':client.metrics})
 freeze(root/'ORG_COMPLETE.json',{'teams':done,'planned':1728,'seconds':time.time()-start,'api':client.metrics,'prior_actual_unknown_requests':len(actual_unknowns),'continuation_not_clean_replication':True})
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--old',required=True);p.add_argument('--root',required=True);a=p.parse_args();run(a.old,a.root)
