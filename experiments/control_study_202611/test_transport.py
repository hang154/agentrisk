import copy,http.server,json,pathlib,tempfile,threading,unittest
from .runner import Client,episode
from .common import wire,ACTOR_SYSTEM,sha
from .tasks import development_bank,gold_actions
from .protocol import initialize,calibration
from .independent import independent_labels

class TransportTests(unittest.TestCase):
 def test_once_only_and_immutable_raw(self):
  state={'posts':0,'error':False}
  class Handler(http.server.BaseHTTPRequestHandler):
   def log_message(self,*a):pass
   def do_POST(self):
    state['posts']+=1;self.rfile.read(int(self.headers['Content-Length']))
    if state['error']:self.send_response(503);self.end_headers();self.wfile.write(b'{"error":"synthetic transport test"}');return
    b=json.dumps({'choices':[{'finish_reason':'stop','message':{'content':'{}'}}],'usage':{'prompt_tokens':3,'completion_tokens':2,'total_tokens':5}}).encode();self.send_response(200);self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
  server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  try:
   with tempfile.TemporaryDirectory() as d:
    c=Client(d,2,f'http://127.0.0.1:{server.server_port}/v1');payload=wire([{'role':'user','content':'offline test'}],1)
    a,r=c.call(payload,'success','offline_test');c.call(payload,'success','offline_test');self.assertEqual(1,state['posts'])
    p=pathlib.Path(d)/'raw/success/response.raw';p.write_text('{}')
    with self.assertRaises(AssertionError):c.call(payload,'success','offline_test')
    state['error']=True
    with self.assertRaises(Exception):c.call(payload,'unknown','offline_test')
    with self.assertRaises(FileExistsError):c.call(payload,'unknown','offline_test')
    self.assertEqual(2,state['posts']);u=json.loads((pathlib.Path(d)/'raw/unknown/UNKNOWN.json').read_text());self.assertEqual(4096,u['maximum_missing_output']);self.assertFalse(u['retry'])
  finally:server.shutdown();server.server_close();thread.join()

 def test_offline_production_semantics_all_policies(self):
  task=development_bank()[0];_,model=calibration()
  class OfflineClient:
   def __init__(self,root):self.root=root;self.step=0
   def call(self,payload,rid,role):
    if role=='pre_action_monitor':action={'decision':'ALLOW','risk_probability':0.0,'reason':'offline instrument positive control'}
    else:
     actions=gold_actions(task)+[dict(tool='finish',subject='',value='',amount=0,reference='',reason='offline completion')];action=actions[self.step];self.step+=1
    return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps(action)}}]},{'id':rid,'finish':'stop','usage':{'completion_tokens':1,'prompt_tokens':1,'total_tokens':2}}
  with tempfile.TemporaryDirectory() as d:
   root=pathlib.Path(d);plan=initialize(root)
   for arm in ['B0','B1','B2','B3','B4']:
    client=OfflineClient(root);r=episode(client,task,'benign',arm,999,model,plan,'OFFLINE_INSTRUMENT_TEST_NOT_SCIENTIFIC')
    self.assertTrue(r['oracle']['task_complete']);rebuilt=independent_labels(task,r['events'],r['final'],r['status'])
    for k,v in rebuilt.items():self.assertEqual(v,r['oracle'][k])
    # Completed episode resume must not invoke client again.
    prior=client.step;self.assertEqual(r,episode(client,task,'benign',arm,999,model,plan,'OFFLINE_INSTRUMENT_TEST_NOT_SCIENTIFIC'));self.assertEqual(prior,client.step)

 def test_interrupted_lease_not_reissued(self):
  with tempfile.TemporaryDirectory() as d:
   root=pathlib.Path(d);plan=initialize(root);t=development_bank()[0];eid=sha([plan['experiment_id'],'pilot',t['task_id'],'benign','B0',1])[:28];(root/'leases').mkdir();(root/'leases'/eid).touch()
   class C:
    def __init__(self):self.root=root
    def call(self,*a):raise AssertionError('MUST_NOT_POST')
   with self.assertRaisesRegex(ValueError,'INCOMPLETE_EPISODE'):episode(C(),t,'benign','B0',1,calibration()[1],plan,'pilot')
if __name__=='__main__':unittest.main()
