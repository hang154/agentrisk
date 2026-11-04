import copy,unittest
from .analysis import forecast_scores,paired
from .baselines import fit,predict

class AnalysisTests(unittest.TestCase):
 def test_baseline_scored_even_if_research_predictor_abstains(self):
  rows=[{'arm':'B0','events':[{'receipt':{'proposal':{'tool':'pay'}},'prediction':{'risk_probability':None,'baseline_beta':.2,'baseline_lr':.3,'baseline_gbdt':.1},'independent_bad_proposal':True}]}]
  r=forecast_scores(rows);self.assertEqual(0,r['risk_probability']['n']);self.assertEqual(1,r['baseline_beta']['n']);self.assertAlmostEqual(.64,r['baseline_beta']['brier'])
 def test_seeds_not_independent_clusters(self):
  rows=[]
  for family in range(3):
   for seed in range(20):
    for arm,unsafe in [('B0',True),('B4',False)]:rows.append({'task_id':str(family),'cluster':str(family),'scenario':'adversarial','seed':seed,'arm':arm,'oracle':{'unsafe_state_transition':unsafe}})
  r=paired(rows,'B4','B0','unsafe_state_transition');self.assertEqual(3,r['clusters']);self.assertEqual(60,r['pairs']);self.assertEqual(-1,r['effect'])
  self.assertEqual(.25,r['exact_two_sided_signflip_p'])
 def test_missing_pair_does_not_become_safe(self):
  rows=[{'task_id':'a','cluster':'f','scenario':'benign','seed':1,'arm':a,'oracle':{'unsafe_state_transition':v}} for a,v in [('B0',True),('B4',None)]]
  r=paired(rows,'B4','B0','unsafe_state_transition');self.assertIsNone(r['effect']);self.assertEqual(1,r['pairs_missing'])
 def test_gbdt_deterministic_probability(self):
  rows=[{'x':[1,float(i%2),0,0,0,0,0],'y':i%2} for i in range(40)];m=fit(rows);self.assertEqual(m,fit(rows));self.assertLess(predict(m,rows[0]['x']),.1);self.assertGreater(predict(m,rows[1]['x']),.9)
if __name__=='__main__':unittest.main()
