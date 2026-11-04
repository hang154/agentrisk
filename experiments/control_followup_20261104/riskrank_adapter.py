"""Portable original Hybrid20 risk model, guarded by exact configuration semantics."""
import json,math,pathlib
DATA=pathlib.Path(__file__).parent/'data/RISKRANK_PORTABLE.json'
MODEL=json.loads(DATA.read_text())
CELLS={tuple(r['x']):(r['sum'],r['n']) for r in MODEL['cells']}
def features(u):
 f=MODEL['family_contracts'][u['family']]
 return [float(u['actor']=='gemma'),float(u['narrow']),float(u['hard']),float(u.get('inheritance','inherit')=='allowlist'),float(u.get('inheritance','inherit')=='escrow'),float(u.get('inheritance','inherit')=='signoff'),float(u.get('limit',1)),u['max_actions']/32,MODEL['depth'][u['topology']]/3]+[float(op in f['operations']) for op in MODEL['operations']]+[float(f['capability']==c) for c in ['write','pay','network','delete']]
def raw_predict(x):
 if len(x)!=60 or any(not math.isfinite(v) for v in x):raise ValueError('INVALID_FEATURE_CONTRACT')
 z=MODEL['init']
 for tree in MODEL['trees']:
  n=0
  while not tree[n]['is_leaf']:
   row=tree[n];n=row['left'] if x[row['feature_idx']]<=row['num_threshold'] else row['right']
  z+=tree[n]['value']
 p=1/(1+math.exp(-z));s,n=CELLS.get(tuple(x),(0,0));return max(1e-8,min(1-1e-8,(s+MODEL['spec']['strength']*p)/(n+MODEL['spec']['strength'])))
def predict(u,attestation=None):
 supported=u.get('family') in MODEL['family_contracts'] and u.get('actor') in ['gemma','gptoss'] and u.get('topology') in ['star4','branch22','deep4'] and u.get('max_actions') in [4,8,16,32] and u.get('narrow') in [0,1] and u.get('hard') in [0,1] and u.get('inheritance','inherit')=='inherit' and u.get('limit',1)==1 and u.get('recovery',0)==0 and u.get('operating_policy','standard')=='standard'
 if not supported:return dict(status='NEEDS_ANCHOR_EVALUATION',risk=None,reason='UNSUPPORTED_WORKFLOW_OR_CONFIGURATION',identity_updates_enabled=False)
 if not attestation or attestation.get('native_contract_revision')!='riskrank-v4-exact-permissions' or attestation.get('effective_operations')!=MODEL['family_contracts'][u['family']]['operations']:
  return dict(status='NEEDS_ANCHOR_EVALUATION',risk=None,reason='UNATTESTED_EXECUTION_SEMANTICS',identity_updates_enabled=False)
 return dict(status='BEST_TESTED_LAB_F0',risk=raw_predict(features(u)),identity_updates_enabled=False,source_model_sha256=MODEL['source_model_sha256'])
