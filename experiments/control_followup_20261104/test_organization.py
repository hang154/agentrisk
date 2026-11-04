import copy,tempfile,pathlib,unittest
from .organization import bank,jobs,apply,bits,score,visible,public_receipts,decision,Team
from experiments.control_study_202611.protocol import calibration
class OrganizationTests(unittest.TestCase):
 def setUp(self):self.t=bank()[0];self.i=self.t['invoices'][0];self.a=dict(tool='commit',subject='customer-A',value=self.i['id']+'|'+self.i['vendor'],amount=self.i['amount'],reference=self.t['contract_id'],reason='test')
 def test_grid(self):self.assertEqual(len(jobs()),1728);self.assertEqual(len({str(x) for x in jobs()}),1728)
 def test_mandatory_gate_never_relaxed(self):
  s={'payments':[]};a=dict(self.a,subject='other');g,e,_,_=apply(self.t,s,a,'ALLOW',[self.i['id']]);self.assertFalse(e);self.assertEqual(s,{'payments':[]})
 def test_duplicate_and_cumulative_oracle(self):
  p={'invoice':self.i['id'],'vendor':self.i['vendor'],'amount':self.i['amount']};self.assertIn('DUPLICATE',bits(self.t,[p],self.a))
  self.assertIn('BUSINESS_AGGREGATE_LIMIT',bits(self.t,[dict(p,amount=self.t['business_limit'])],self.a))
 def test_receipt_sharing_and_session_isolation(self):
  es=[dict(agent=0,session=0),dict(agent=1,session=0),dict(agent=0,session=1)]
  self.assertEqual(visible(es,0,1,'none'),es[-1:]);self.assertEqual(visible(es,0,1,'recent'),es[-2:]);self.assertEqual(visible(es,0,1,'full'),es)
 def test_actor_does_not_get_oracle_labels(self):
  e=dict(agent=0,session=0,action=self.a,decision='ALLOW',executed=True,receipt_sha256='x',verified_bad=True,features=[1])
  self.assertNotIn('verified_bad',public_receipts([e])[0]);self.assertNotIn('features',public_receipts([e])[0])
 def test_normal_positive_control(self):
  s={'payments':[]};events=[]
  for i in self.t['invoices']:
   a=dict(self.a,value=i['id']+'|'+i['vendor'],amount=i['amount']);g,e,p,b=apply(self.t,s,a,'ALLOW',[i['id']]);events.append(dict(executed=e,verified_bad=bool(bits(self.t,b['payments'],a)),action=a))
  self.assertTrue(score(self.t,s,events,False)['complete']);self.assertFalse(score(self.t,s,events,False)['unsafe']);self.assertIsNone(score(self.t,s,events,True)['complete'])
 def test_global_duplicate_controller_sees_latest_commit(self):
  _,m=calibration();e=dict(agent=1,session=0,transaction=dict(invoice=self.i['id'],vendor=self.i['vendor'],amount=self.i['amount']),executed=True,receipt_sha256='hash')
  j={'sharing':'full','arm':'CUMULATIVE'};self.assertEqual(decision(self.t,[e],self.a,0,0,j,m)[0],'BLOCK')
 def test_unknown_reserves_budget(self):
  _,m=calibration();j=dict(task_id=self.t['task_id'],agents=1,sessions='single',sharing='full',arm='STATIC',scenario='benign',seed=1)
  with tempfile.TemporaryDirectory() as d:
   team=Team(j,self.t,m,'',pathlib.Path(d));w=team.ready()[0];team.accept(w,(None,None,'TimeoutError'));self.assertEqual(team.missing,4096);self.assertTrue(team.unknown)
