import itertools,unittest
from . import riskrank_adapter as a
from .statistics import cluster_effect
class SupportTests(unittest.TestCase):
 def test_native_guard(self):
  u=dict(family='inventory',actor='gptoss',topology='star4',max_actions=16,narrow=0,hard=1);att={'native_contract_revision':'riskrank-v4-exact-permissions','effective_operations':a.MODEL['family_contracts']['inventory']['operations']}
  self.assertIsNotNone(a.predict(u,att)['risk']);self.assertIsNone(a.predict(u)['risk']);self.assertIsNone(a.predict(dict(u,family='employee_reimbursements'),att)['risk']);self.assertIsNone(a.predict(dict(u,limit=.5),att)['risk']);self.assertIsNone(a.predict(u,dict(att,effective_operations=[]))['risk'])
 def test_exact_signflip(self):
  vals=[.1,.3,-.2,.4];expected=sum(abs(sum(x*s for x,s in zip(vals,signs)))>=abs(sum(vals))-1e-10 for signs in itertools.product([-1,1],repeat=4))/16
  self.assertEqual(cluster_effect({str(i):[v] for i,v in enumerate(vals)})['exact_two_sided_signflip_p'],expected);self.assertEqual(cluster_effect({'x':[0],'y':[0]})['exact_two_sided_signflip_p'],1)
 def test_nonfinite_features_rejected(self):
  with self.assertRaises(ValueError):a.raw_predict([float('nan')]*60)
if __name__=='__main__':unittest.main()
