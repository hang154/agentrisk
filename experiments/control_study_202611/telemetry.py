"""Read-only GPU2/owned engine telemetry, separate from scientific outcomes."""
import json,os,pathlib,subprocess,threading,time,urllib.request
from .common import update

class Telemetry:
 def __init__(self,root,tag):self.root=pathlib.Path(root);self.tag=tag;self.stop=threading.Event();self.thread=None
 def start(self):self.thread=threading.Thread(target=self.run,daemon=True);self.thread.start();return self
 def close(self):self.stop.set();self.thread.join(timeout=6)
 def run(self):
  path=self.root/'telemetry'/f'{self.tag}.jsonl';path.parent.mkdir(exist_ok=True)
  while not self.stop.is_set():
   row={'epoch':time.time(),'loadavg':os.getloadavg(),'uid':os.getuid(),'allowed_cpus':sorted(os.sched_getaffinity(0)),'fd_count':len(list(pathlib.Path('/proc/self/fd').iterdir()))}
   try:
    raw=urllib.request.urlopen('http://127.0.0.1:18531/metrics',timeout=2).read().decode()
    row['engine_metrics']=[s for s in raw.splitlines() if not s.startswith('#') and any(k in s for k in ['num_requests_running','num_requests_waiting','kv_cache_usage_perc','num_preemptions_total','prefix_cache','generation_tokens_total','prompt_tokens_total'])]
    row['gpu2']=subprocess.check_output(['nvidia-smi','-i','2','--query-gpu=uuid,utilization.gpu,utilization.memory,memory.used,power.draw','--format=csv,noheader,nounits'],text=True,timeout=3).strip()
   except Exception as e:row['error']=type(e).__name__
   with path.open('a') as f:f.write(json.dumps(row)+'\n')
   self.stop.wait(5)
