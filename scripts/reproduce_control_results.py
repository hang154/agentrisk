#!/usr/bin/env python3
"""No GPU or network needed. Rebuild results from released real episode samples."""
import argparse,json,pathlib,sys,tempfile,shutil
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from experiments.control_study_202611.independent import audit
from experiments.control_study_202611.analysis import analyze
from experiments.control_study_202611.audit_monitor_evidence import audit_monitors
from experiments.control_study_202611.reproduction_compare import assert_equivalent
from experiments.control_study_202611.supplementary import supplement
p=argparse.ArgumentParser();p.add_argument('evidence');a=p.parse_args()
root=pathlib.Path(a.evidence).resolve()
with tempfile.TemporaryDirectory() as d:
 dst=pathlib.Path(d)/'evidence';shutil.copytree(root,dst)
 for n in ['INDEPENDENT_REPRODUCTION.json','RESULTS.json','PAIRED_CONTROL_EFFECTS.json','UNSEEN_WORKFLOW_EVALUATION.json','RISK_UTILITY_FRONTIER.json']:
  if (dst/n).exists():(dst/n).unlink()
 check=audit(dst);monitors=audit_monitors(dst,write=False);result=analyze(dst)
 if (root/'RESULTS.json').exists():assert_equivalent(result,json.loads((root/'RESULTS.json').read_text()))
 if (root/'CALIBRATION_AND_SCORE_SENSITIVITY.json').exists():assert_equivalent(supplement(dst,write=False),json.loads((root/'CALIBRATION_AND_SCORE_SENSITIVITY.json').read_text()))
 print(json.dumps({'pass':True,'episodes_checked':check['episodes_checked'],'main_rows':result['rows'],'monitor_rows_checked':monitors['rows_checked'],'discrete_results':'EXACT','float_absolute_tolerance':1e-12},indent=2))
