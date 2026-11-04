"""Bounded production-shaped interface/capacity measurements on development tasks.

Diagnostic replay requests are never counted as study episodes. Same schema,
reasoning and budget as production. Report best tested, not hardware maximum.
"""
import concurrent.futures,json,pathlib,time
from .common import freeze,sha,file_sha,wire,ACTOR_SYSTEM,ACTION_SCHEMA
from .tasks import public_task
from .runner import Client,parse,preflight
from .telemetry import Telemetry

def run(root):
 root=pathlib.Path(root);plan=json.loads((root/'PROTOCOL_LOCK.json').read_text());bank=json.loads((root/'DEVELOPMENT_BANK.json').read_text())
 pilots=[json.loads(p.read_text()) for p in (root/'episodes').glob('*.json')];pilots=[r for r in pilots if r['stage']=='pilot']
 assert len(pilots)==40 and all(r['oracle']['known'] for r in pilots),'PILOT_INCOMPLETE_OR_UNKNOWN'
 assert {r['arm'] for r in pilots}==set(plan['policies'])
 assert all(r['calls'] for r in pilots),'NO_REAL_API_CALL'
 assert all(r['events'] for r in pilots),'NO_REAL_TOOL_RECEIPTS'
 # Freeze 512 development request/seed combinations; diagnostic repetitions,
 # not 512 independent scientific sources. No input padding.
 payloads=[]
 for i in range(512):
  t=bank[i%len(bank)];scenario=plan['scenarios'][(i//len(bank))%2]
  messages=[{'role':'system','content':ACTOR_SYSTEM},{'role':'user','content':json.dumps({'task':public_task(t,scenario),'observations':[],'remaining_steps':plan['max_steps']})}]
  payloads.append(wire(messages,7100+i,max_tokens=plan['per_call_output']))
 freeze(root/'CAPACITY_INPUTS.json',payloads)
 records=[]
 def trial(c,rep):
  destination=root/f'CAPACITY_C{c}_R{rep}.json'
  if destination.exists():
   receipt=json.loads(destination.read_text());assert receipt['same_workload_sha256']==sha(payloads);records.append(receipt);return receipt
  preflight(root,c);client=Client(root,c);start=time.time()
  def one(pair):
   i,payload=pair;v,r=client.call(payload,f'capacity-c{c}-r{rep}-{i}','capacity')
   try:parse(v,r,ACTION_SCHEMA);valid=True
   except (ValueError,TypeError,KeyError,AssertionError):valid=False
   return {'valid':valid,'receipt':r}
  telemetry=Telemetry(root,f'capacity_C{c}_R{rep}').start()
  try:
   with concurrent.futures.ThreadPoolExecutor(max_workers=c) as pool:rows=list(pool.map(one,enumerate(payloads)))
  finally:telemetry.close()
  seconds=time.time()-start;valid=sum(r['valid'] for r in rows);tokens=sum(r['receipt']['usage']['total_tokens'] for r in rows);outs=sum(r['receipt']['usage']['completion_tokens'] for r in rows)
  receipt={'concurrency':c,'repeat':rep,'requests':len(rows),'valid':valid,'seconds':seconds,'api_tok_s':tokens/seconds,'output_tok_s':outs/seconds,'valid_responses_s':valid/seconds,'rows':rows,'same_workload_sha256':sha(payloads)}
  freeze(root/f'CAPACITY_C{c}_R{rep}.json',receipt);records.append(receipt);return receipt
 for c in [64,128,256]:trial(c,0)
 stable=[r for r in records if r['valid']/r['requests']>=.99]
 if not stable:raise ValueError('NO_FORMAT_COMPLETE_CAPACITY_PROFILE')
 best=max(stable,key=lambda r:r['valid_responses_s'])
 # The finite scientific population is 800; 256 is the bounded initial search.
 # Expand if still improving, up to actual independent runnable population.
 if best['concurrency']==256 and best['valid_responses_s']>next(r for r in records if r['concurrency']==128)['valid_responses_s']*1.05:
  r=trial(512,0)
  if r['valid']/len(payloads)>=.99 and r['valid_responses_s']>best['valid_responses_s']:best=r
 selected=best['concurrency']
 # Persist exact trial sample counts; trial's stable eligibility is checked by
 # actual row count, including the optional extended sample.
 repeats=[trial(selected,1),trial(selected,2)]
 assert all(r['valid']/len(r['rows'])>=.99 for r in repeats),'REPEATED_FORMAT_COVERAGE_BELOW_PREREGISTERED_99_PERCENT'
 lock={'status':'BEST_TESTED_NEW_WORKLOAD','concurrency':selected,'actual_worker_pool':selected,'actual_http_semaphore':selected,'protocol_sha256':sha(plan),'semantic_e2e_pass':True,
 'server_start_sha256':file_sha(root/'SERVER_START.json'),'selected_capacity_files':[f'CAPACITY_C{selected}_R{i}.json' for i in [0,1,2]],
 'test_range':[r['concurrency'] for r in records if r['repeat']==0],'validity_threshold':.99,'saturation_ceiling_claim':False,'capacity_is_not_scientific_tps':True,'pilot_episodes':40}
 lock['raw_evidence_sha256']={f:file_sha(root/f) for f in lock['selected_capacity_files']};freeze(root/'INFERENCE_LOCK.json',lock);return lock
if __name__=='__main__':
 import sys;print(json.dumps(run(sys.argv[1]),indent=2))
