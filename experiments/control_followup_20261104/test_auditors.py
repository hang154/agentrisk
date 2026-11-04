import copy,json,pathlib,tempfile,time,unittest
from experiments.control_study_202611.common import freeze,sha,file_sha
from . import riskquote_ablation as r,audit_components as audit
from .trajectory_export import export

def fixture(root):
 s=r.Stream('overtime_pay',8101,dict(predictor='AR',supplier='fixed',authority='fixed',history='frozen'),root)
 s.newtrade()
 for operation in ['delegate','propose','approve','commit']:
  _,q,rid,role=s.work();a={'operation':operation,'reason':'unit fixture; never scientific data'}
  if role in ['executor','settlement']:a.update(vendor=s.c['expected_vendor'],invoice=s.c['public']['invoice'],amount=s.c['expected_amount'],idempotency_key=s.eid)
  z={'choices':[{'message':{'role':'assistant','content':json.dumps(a)},'finish_reason':'stop'}],'usage':{'prompt_tokens':10,'completion_tokens':10,'total_tokens':20}}
  d=root/'raw'/rid;freeze(d/'request.json',q);freeze(d/'response.raw',z);freeze(d/'response.json',z);freeze(d/'dispatch.json',{'payload_sha256':sha(q),'time':time.time()})
  c={'id':rid,'role':role,'request_sha256':file_sha(d/'request.json'),'raw_sha256':file_sha(d/'response.raw'),'usage':z['usage'],'finish':'stop'};freeze(d/'receipt.json',c);s.accept((z,c,None))
 s.finish();return s.rows[0]

class AuditorTests(unittest.TestCase):
 def test_empty_cannot_pass_full_grid(self):
  with tempfile.TemporaryDirectory() as t:
   with self.assertRaises(AssertionError):audit.audit(t,write=False)
 def test_fixture_full_raw_partial_audit(self):
  with tempfile.TemporaryDirectory() as t:
   root=pathlib.Path(t);fixture(root);x=audit.audit(root,require_full=False,write=False)
   self.assertEqual(x['raw_calls'],4);self.assertFalse(x['full_grid_checked'])
 def test_raw_tampering_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   root=pathlib.Path(t);row=fixture(root);d=root/'raw'/row['calls'][0]['id']/'response.raw';d.write_text('{}')
   with self.assertRaises(AssertionError):audit.audit(root,require_full=False,write=False)
 def test_state_tampering_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   row=fixture(pathlib.Path(t));row['after']['payments'].append({'vendor':'other','invoice':'fake','amount':1})
   with self.assertRaises(AssertionError):audit.reconstruct(row)
 def test_forecast_tampering_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   root=pathlib.Path(t);row=fixture(root);p=root/'forecast_locks'/f"{row['id']}.json";x=json.loads(p.read_text());x['pre_state_sha256']='tampered';p.write_text(json.dumps(x))
   with self.assertRaises(AssertionError):audit.audit(root,require_full=False,write=False)
 def test_trajectory_actual_context_and_models(self):
  with tempfile.TemporaryDirectory() as t:
   root=pathlib.Path(t)/'evidence';fixture(root);out=pathlib.Path(t)/'export';v=export(root,out);self.assertEqual(v['raw_calls'],4)
   x=json.loads((out/'trajectory.jsonl').read_text());self.assertEqual(len(x['metadata']['request_segments']),4);self.assertEqual(len(x['models']),4);self.assertTrue(json.loads(x['raw_state']))
if __name__=='__main__':unittest.main()
