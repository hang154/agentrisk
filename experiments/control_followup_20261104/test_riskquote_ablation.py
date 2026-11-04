import copy,json,unittest
from . import riskquote_ablation as r
class TestComponents(unittest.TestCase):
 def test_grid_and_shared_candidates(self):
  self.assertEqual(len(r.arms()),17);self.assertEqual(24*2*17*6,4896);self.assertEqual(len(r.SUPPLIERS),5)
  self.assertTrue(all(p['public']['actor']=='gptoss' for p in r.SUPPLIERS));self.assertEqual(len({(p['public']['depth'],p['style']) for p in r.SUPPLIERS}),5)
 def test_model_features_and_scores(self):
  for f in r.TEST:
   c=r.contract(f,8101,'ablation-shared-customer',0)
   for p in r.SUPPLIERS:
    for kind in ['AR','GB']:
     q=r.quote(c,p,'pay',25,[],kind);self.assertEqual(len(q['features']),76);self.assertTrue(all(0<=v<=1 for v in q['predictions'].values()))
 def test_public_has_no_oracle(self):
  c=r.contract(r.TEST[0],8101,'x',0);q=r.choose(c,r.arms()[0],{p['id']:[] for p in r.SUPPLIERS},300)['selected']
  messages=r.role_input(c,r.SUPPLIERS[0],'executor',{},q,'x');s=json.dumps(messages)
  self.assertNotIn('expected_amount',s);self.assertNotIn('canonical',s)
 def test_typed_history_does_not_misuse_read_success(self):
  c=r.contract(r.TEST[0],8101,'x',0);p=r.SUPPLIERS[0];base=r.quote(c,p,'pay',25,[],'AR')
  h=[dict(id='read',status='complete',workflow=c['source_root'],mode='read',limit=0,success=True,material=None)]
  self.assertEqual(base,r.quote(c,p,'pay',25,h,'AR'))
 def test_gateway_and_oracle(self):
  c=r.contract('overtime_pay',8101,'x',0);due=c['expected_amount'];q={'mode':'pay','limit':50};roles={'manager':{'operation':'delegate'},'reviewer':{'operation':'approve'},'executor':{'operation':'propose','vendor':c['expected_vendor'],'invoice':c['public']['invoice'],'amount':due},'settlement':{'operation':'commit','vendor':c['expected_vendor'],'invoice':c['public']['invoice'],'amount':due,'idempotency_key':'test'}}
  state={'payments':[]};a,g,t,o=r.settle(c,roles,q,state,'test',True,0);self.assertTrue(o['success']);self.assertFalse(o['material']);self.assertEqual(g,'ALLOW');self.assertEqual(state,{'payments':[]})
  a,g,t,o=r.settle(c,roles,dict(q,mode='read'),state,'test',True,0);self.assertEqual(g,'DENIED_SCOPE');self.assertEqual(a,state)
  roles['settlement']['amount']+=1;a,g,t,o=r.settle(c,roles,q,state,'test',True,0);self.assertEqual(o['material'],1);self.assertEqual(o['loss'],1)
 def test_unknown_is_not_zero(self):
  c=r.contract(r.TEST[0],8101,'x',0);a,g,t,o=r.settle(c,{},dict(mode='pay',limit=50),{'payments':[]},'x',False,0)
  self.assertIsNone(o['success']);self.assertIsNone(o['loss']);self.assertIsNone(o['material'])
 def test_fixed_choice_constraints(self):
  c=r.contract(r.TEST[0],8101,'x',1);h={p['id']:[] for p in r.SUPPLIERS};q=r.choose(c,r.arms()[0],h,300)
  self.assertEqual(len({x['candidate'] for x in q['options']}),1);self.assertTrue(all(x['limit']<=50 for x in q['options']))
 def test_contract_oracle_all_roots(self):
  for f in r.TEST:
   for seed in [8101,8102]:
    for i in range(6):
     c=r.contract(f,seed,'ablation-shared-customer',i);self.assertEqual(c['expected_amount'],r.independent_due(f,c['canonical']['data']))
if __name__=='__main__':unittest.main()
