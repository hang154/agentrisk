import copy,json,pathlib,tempfile,unittest
from .common import sha,freeze,MONITOR_SCHEMA,ACTION_SCHEMA
from .tasks import build_bank,development_bank,gold_actions,public_task
from .setting import execute,hard_gate,initial_state,verify_receipts
from .oracle import score,violations
from .policies import Control,features
from .protocol import calibration,oracle_controls
from .monitors import pre_action,post_action

class StudyTests(unittest.TestCase):
 def setUp(self):self.t=build_bank()[0];self.a=gold_actions(self.t)[0]
 def test_population_and_separation(self):
  tasks=build_bank();self.assertEqual(40,len(tasks));self.assertEqual(10,len({t['cluster'] for t in tasks}))
  self.assertFalse({t['task_id'] for t in tasks}&{t['task_id'] for t in development_bank()})
  self.assertEqual(16,sum(t['split']=='heldout_source' for t in tasks))
 def test_all_oracle_positive_negative_controls(self):self.assertEqual(44,len(oracle_controls()))
 def test_mutable_receipts_are_copied(self):
  s=initial_state();_,r=execute(self.t,s,self.a);old=sha(r);s['records'].clear();self.a['value']='other';self.assertEqual(old,sha(r))
 def test_tamper_rejected(self):
  s=initial_state();h=sha(s);_,r=execute(self.t,s,self.a);e={'pre_state_sha256':h,'receipt':r}
  self.assertTrue(verify_receipts(initial_state(),[e],s));r['after']['cash_exposure']+=1
  with self.assertRaises(ValueError):verify_receipts(initial_state(),[e],s)
 def test_b4_cannot_relax_hardgate(self):
  _,m=calibration();c=Control('B4',m);s=initial_state();a=dict(self.a,subject='other-customer');d,_=c.decide(self.t,s,a);_,r=execute(self.t,s,a,d)
  self.assertFalse(r['executed']);self.assertEqual(initial_state(),s)
 def test_blocked_attempt_not_incident(self):
  s=initial_state();a=dict(self.a,value='bad');h=sha(s);_,r=execute(self.t,s,a,'BLOCK');o=score(self.t,initial_state(),[{'receipt':r}],s,'FINISH')
  self.assertEqual(1,o['bad_proposals']);self.assertFalse(o['unsafe_state_transition']);self.assertEqual(0,o['synthetic_direct_loss_units'])
 def test_unknown_is_not_zero(self):
  o=score(self.t,initial_state(),[],initial_state(),'UNKNOWN');self.assertIsNone(o['task_complete']);self.assertIsNone(o['unsafe_state_transition']);self.assertIsNone(o['synthetic_direct_loss_units'])
 def test_allblock_fails_utility(self):
  s=initial_state();events=[]
  for a in gold_actions(self.t):_,r=execute(self.t,s,a,'BLOCK');events.append({'receipt':r})
  o=score(self.t,initial_state(),events,s,'FINISH');self.assertFalse(o['task_complete']);self.assertFalse(o['unsafe_state_transition']);self.assertGreater(o['false_blocks'],0)
 def test_adaptive_only_past_updates(self):
  _,m=calibration();f=Control('B3',m);a=Control('B4',m);x=features(self.t,initial_state(),self.a);p=a.prediction(x)
  a.observe(x,True,'prior-receipt');self.assertGreater(a.prediction(x),p);self.assertEqual(p,f.prediction(x))
  self.assertEqual(sha(m),sha(f.model));self.assertNotEqual(sha(m),sha(a.model))
 def test_pre_action_no_future_label(self):
  text=json.dumps(pre_action(self.t,initial_state(),self.a,[]));self.assertNotIn('executed_bad',text);self.assertNotIn('oracle',text);self.assertNotIn('after',text)
 def test_post_action_views_and_future_separation(self):
  s=initial_state();_,r=execute(self.t,s,self.a);e={'receipt':r,'executed_bad':'HIDDEN_GOLD'}
  for c in ['M0','M1','M2','M3','M2_PROSE']:
   text=json.dumps(post_action(self.t,e,[],c));self.assertNotIn('HIDDEN_GOLD',text)
   if c=='M0':self.assertNotIn('structured_proposal',text)
   if c=='M1':self.assertNotIn('trusted_execution_receipt',text)
 def test_nonmutation_no_damage(self):
  s=initial_state();a=dict(self.a,tool='read');_,r=execute(self.t,s,a);self.assertEqual(initial_state(),s);self.assertFalse(r['executed'])
 def test_duplicate_execution_detected(self):
  s=initial_state();execute(self.t,s,self.a);self.assertIn('DUPLICATE_EXECUTION',violations(self.t,s,self.a))
 def test_predecessor_corruption_detected(self):
  s=initial_state();execute(self.t,s,dict(self.a,value='wrong'));self.assertIn('INVALID_PREREQUISITE_STATE',violations(self.t,s,gold_actions(self.t)[1]))
 def test_new_root_no_leakage(self):
  _,m=calibration();c=Control('B4',m);x=features(self.t,initial_state(),self.a);c.observe(x,True,'r');fresh=Control('B4',m);self.assertEqual(0,len(fresh.updates));self.assertEqual(sha(m),sha(fresh.model))
 def test_immutable_artifact(self):
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d)/'lock.json';freeze(p,{'x':1});freeze(p,{'x':1})
   with self.assertRaises(ValueError):freeze(p,{'x':2})
 def test_identity_gate(self):
  for a in [dict(self.a,tool='shell'),dict(self.a,reference='other'),dict(self.a,amount=101),dict(self.a,subject='another')]:self.assertNotEqual('ALLOW',hard_gate(self.t,a))
 def test_deterministic_controls(self):self.assertEqual(sha(calibration()),sha(calibration()))
 def test_no_test_labels_in_actor(self):
  for t in build_bank():
   x=public_task(t,'adversarial');self.assertNotIn('oracle',x);self.assertNotIn('unsafe_state_transition',json.dumps(x));self.assertNotIn('risk_probability',json.dumps(x))
if __name__=='__main__':unittest.main()
