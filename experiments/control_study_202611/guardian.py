"""Durable single supervisor; waits for owned GPU2 server, never stops services.

No automatic semantic-failure restart. Completed stages are skipped; interrupted
POSTs retain their IDs and fail closed. Launch only after committed source lock.
"""
import argparse,fcntl,json,os,pathlib,subprocess,sys,time,urllib.request
from .common import freeze,update,file_sha

def run(root):
 root=pathlib.Path(root);lock=(root/'GUARDIAN.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 plan=json.loads((root/'PROTOCOL_LOCK.json').read_text());commit=json.loads((root/'PREREGISTRATION_COMMIT.json').read_text())
 assert commit['commit'] and commit['remote_verified']
 for name,digest in plan['source_sha256'].items():assert file_sha(pathlib.Path(__file__).parent/name)==digest,('SOURCE_CHANGED',name)
 assert json.loads((root/'UNIT_TESTS.json').read_text())['passed']
 if (root/'GUARDIAN_FAILURE.json').exists():raise RuntimeError('EXPLICIT_FAILURE_REVIEW_REQUIRED')
 if not (root/'SUPERVISION_START.json').exists():freeze(root/'SUPERVISION_START.json',{'pid':os.getpid(),'gpu':2,'commit':commit['commit'],'no_automatic_restart':True})
 freeze(root/'supervision_attempts'/f'{time.time_ns()}.json',{'pid':os.getpid(),'epoch':time.time(),'commit':commit['commit']})
 try:
  for _ in range(2880):
   if (root/'RESOURCE_COORDINATION_HOLD.json').exists():
    update(root/'SUPERVISION.json',{'stage':'WAIT_GPU2_OWNERSHIP_CLARIFICATION','epoch':time.time(),'model_requests_dispatched':0});time.sleep(15);continue
   s=json.loads((root/'SERVER_STATUS.json').read_text()) if (root/'SERVER_STATUS.json').exists() else {}
   update(root/'SUPERVISION.json',{'stage':'WAIT_OWNED_GPU2_SERVER','server_stage':s.get('stage'),'epoch':time.time(),'main_completed':0,'main_planned':800})
   if s.get('stage') in ['FAILED','ENGINE_DIED']:raise RuntimeError('SERVER_FAILED_NO_AUTORESTART')
   if s.get('stage')=='READY':
    assert s['gpu']==2
    with urllib.request.urlopen('http://127.0.0.1:18531/health',timeout=3) as r:assert r.status==200
    break
   time.sleep(15)
  else:raise RuntimeError('GPU2_AVAILABILITY_EXTERNAL_WAIT_EXCEEDED')
  def stage(name,module,args,done):
   if (root/done).exists():return
   argv=[sys.executable,'-m','experiments.control_study_202611.'+module,*args]
   with (root/(name+'.log')).open('ab',buffering=0) as log:
    child=subprocess.Popen(argv,stdout=log,stderr=log,stdin=subprocess.DEVNULL)
   last_progress=time.monotonic();previous=None
   while child.poll() is None:
    counts={'episode_files':len(list((root/'episodes').glob('*.json'))),'raw_responses':len(list((root/'raw').glob('*/response.json'))),'monitor_rows':len(list((root/'monitor_results').glob('*.json'))),'unknown_requests':len(list((root/'raw').glob('*/UNKNOWN.json')))}
    if counts!=previous:last_progress=time.monotonic();previous=counts
    stall=time.monotonic()-last_progress
    if stall>900 and name in ['PILOT','CERTIFICATION','MAIN','POST_ACTION_MONITORS']:(root/'STOP_NEW_DISPATCH').touch(exist_ok=True)
    update(root/'SUPERVISION.json',{'stage':name,'child_pid':child.pid,'epoch':time.time(),'gpu':2,'automatic_restart':False,'progress':counts,'seconds_without_progress':stall,'admission_hold':(root/'STOP_NEW_DISPATCH').exists()})
    time.sleep(10)
   if child.returncode:raise RuntimeError(name+'_FAILED_EXIT_'+str(child.returncode))
   assert (root/done).exists(),('MISSING_STAGE_OUTPUT',name)
  stage('PILOT','runner',['--root',str(root),'--stage','pilot','--concurrency','64'],'PILOT_COMPLETE.json')
  stage('CERTIFICATION','certify',[str(root)],'INFERENCE_LOCK.json')
  c=json.loads((root/'INFERENCE_LOCK.json').read_text())['concurrency']
  stage('MAIN','runner',['--root',str(root),'--stage','main','--concurrency',str(c)],'MAIN_COMPLETE.json')
  stage('POST_ACTION_MONITORS','runner',['--root',str(root),'--stage','monitors','--concurrency',str(c)],'MONITOR_COMPLETE.json')
  stage('INDEPENDENT_AUDIT','independent',[str(root)],'INDEPENDENT_REPRODUCTION.json')
  stage('ANALYSIS','analysis',[str(root)],'RESULTS.json')
  stage('REPORT','report',[str(root)],'FINAL_STATUS.json')
  update(root/'SUPERVISION.json',{'stage':'EXPERIMENT_AND_ANALYSIS_FINISHED','epoch':time.time(),'gpu':2,'backup_pending':True,'model_left_running':True})
 except Exception as e:
  freeze(root/'GUARDIAN_FAILURE.json',{'epoch':time.time(),'error':type(e).__name__+':'+str(e),'automatic_restart':False,'requests_reissued':False})
  update(root/'SUPERVISION.json',{'stage':'HALTED_FOR_DIAGNOSIS','error':str(e),'epoch':time.time()});raise
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root');a=p.parse_args();run(a.root)
