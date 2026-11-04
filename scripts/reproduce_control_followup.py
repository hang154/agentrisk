#!/usr/bin/env python3
"""Recompute released follow-up evidence without GPU calls or dependencies."""
import argparse,json,pathlib,sys,time
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from experiments.control_followup_20261104 import audit_census,audit_attacker,audit_organizations,audit_components
from experiments.control_study_202611.reproduction_compare import assert_equivalent

def main():
 p=argparse.ArgumentParser();p.add_argument('--evidence',required=True);p.add_argument('--v1',required=True);p.add_argument('--output',required=True);a=p.parse_args();root=pathlib.Path(a.evidence);v1=pathlib.Path(a.v1);repo=pathlib.Path(__file__).resolve().parents[1];reports=repo/'artifacts/control_followup_20261104';start=time.time();checks={}
 jobs=[('census',lambda:audit_census.audit(root/'census',v1,write=False),'MONITOR_CENSUS.json'),('attacker',lambda:audit_attacker.audit(root/'attacker',v1,root/'organizations',write=False),'ADAPTIVE_ATTACKER_AUDIT.json'),('organizations',lambda:audit_organizations.audit(root/'organizations_continuation',write=False),'ORGANIZATION_REPRODUCTION.json'),('components',lambda:audit_components.audit(root/'components_schema_v2',write=False),'COMPONENT_REPRODUCTION.json')]
 for name,fn,filename in jobs:
  result=json.loads(json.dumps(fn()));assert_equivalent(result,json.loads((reports/filename).read_text()));checks[name]={'pass_gate':True,'raw_calls':result.get('raw_calls',result.get('raw_calls_verified',result.get('new_calls')))};print(name,'PASS',flush=True)
 old=audit_components.audit(root/'components',require_full=False,write=False);assert old['pilot_trades']==17 and old['raw_calls']==68;checks['failed_original_pilot']={'raw_reconstruction':True,'scientific_samples':0}
 result={'pass_gate':True,'checks':checks,'seconds':time.time()-start,'discrete_exact':True,'float_tolerance':1e-12,'new_model_requests':0};pathlib.Path(a.output).write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
