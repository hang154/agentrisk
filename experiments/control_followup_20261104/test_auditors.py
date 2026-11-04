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
 def test_unknown_invoice_counts_excluded_from_utility_pairs(self):
  from .audit_organizations import analyze
  rows=[]
  for arm in ['STATIC','CUMULATIVE','FROZEN','ADAPTIVE']:
   for i in [0,1]:
    known=not (arm=='ADAPTIVE' and i==1)
    rows.append({'job':dict(task_id=str(i),agents=1,sessions='single',sharing='full',scenario='benign',seed=1,arm=arm),'cluster':'same_mechanism','calls':[],'output_tokens':0,'score':dict(known=known,complete=True if known else None,correct_invoices=12 if known else 0,unsafe=False if known else None,synthetic_loss=0 if known else None,false_blocks=0,unsafe_transitions_observed=0)})
  panel=analyze(rows)['paired']['CUMULATIVE']
  self.assertEqual(panel['correct_invoices']['pairs'],1);self.assertEqual(panel['correct_invoices']['effect'],0)
  self.assertIsNone(panel['unsafe']['cluster_bootstrap_ci95']);self.assertIsNone(panel['unsafe']['exact_two_sided_signflip_p']);self.assertFalse(panel['safety_utility_success'])
 def test_old_interface_is_explicit_and_unknown_rejected(self):
  c=r.contract('overtime_pay',8101,'ablation-shared-customer',0);p=r.SUPPLIERS[0];q={'mode':'pay','limit':50}
  old=audit.expected_messages(c,p,'manager',{},q,'x','riskquote-component-v1')
  self.assertTrue(old[0]['content'].endswith('Return the required JSON.'));self.assertNotIn('Required JSON schema:',old[0]['content'])
  with self.assertRaises(ValueError):audit.expected_messages(c,p,'manager',{},q,'x','unknown')
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
