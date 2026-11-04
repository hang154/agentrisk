import copy,unittest,tempfile,pathlib,json,subprocess,os,sys
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
 def test_analysis_stable_across_hash_seeds_and_file_order(self):
  with tempfile.TemporaryDirectory() as d:
   results=[]
   for seed,order in [('1',range(40)),('2',reversed(range(40)))]:
    root=pathlib.Path(d)/seed;(root/'episodes').mkdir(parents=True);(root/'monitor_results').mkdir()
    for i in order:
     for condition in ['M0','M2']:
      r={'episode_id':str(i),'condition':condition,'status':'VALID','cluster':str(i%10),'target_actual_unsafe_execution':bool(i%3),'verdict':{'decision':'ALLOW','risk_probability':(i%7)/10+(.1 if condition=='M0' else 0)}}
      (root/'monitor_results'/f'{i}-{condition}.json').write_text(json.dumps(r))
    env=os.environ.copy();env['PYTHONHASHSEED']=seed
    subprocess.run([sys.executable,'-m','experiments.control_study_202611.analysis',str(root)],check=True,stdout=subprocess.DEVNULL,env=env)
    results.append(json.loads((root/'RESULTS.json').read_text()))
   self.assertEqual(*results)
if __name__=='__main__':unittest.main()
