"""Pre-action controls with equal public contract/state visibility.

Risk predictors use observable features, never post-action labels. The adaptive
posterior is episode-local: a later root cannot leak into an earlier decision.
"""
import copy,math
from .common import sha

def features(task,state,a):
 spec=next((s for s in task['steps'] if s['tool']==a['tool']),None)
 past={e['tool'] for e in state['journal']}
 # Deliberately no value-equals-gold feature. This is not an oracle in disguise.
 return [1.0,min(a['amount']/max(1,task['per_action_limit']),2),float(a['tool'] in past),
  float(bool(spec) and any(r not in past for r in spec['requires'])),
  min((state['cash_exposure']+a['amount'])/max(1,task['cumulative_limit']),3),
  float(bool(spec) and spec['amount']==0 and a['amount']>0),
  min(len(state['journal'])/max(1,len(task['steps'])),2)]

def bucket(x):return str((int(x[2]),int(x[3]),int(x[4]>1),int(x[5])))
def train(rows):
 from .baselines import fit
 # Frozen Beta buckets + ridge logistic baseline, no package dependency.
 counts={};w=[0.0]*7
 for r in rows:
  b=bucket(r['x']);counts.setdefault(b,[1.0,1.0]);counts[b][int(not r['y'])]+=1
 for it in range(800):
  gradient=[0.2*v for v in w]
  for r in rows:
   p=logistic(w,r['x'])
   for j,x in enumerate(r['x']):gradient[j]+=(p-r['y'])*x
  for j in range(len(w)):w[j]-=0.8*gradient[j]/max(1,len(rows))
 model={'revision':'observable-beta-buckets-v1','counts':counts,'global':[1+sum(r['y'] for r in rows),1+sum(1-r['y'] for r in rows)],'lr_weights':w,'gbdt':fit(rows),'n':len(rows),'training_sha256':sha(rows)}
 normal=[counts[bucket(r['x'])][0]/sum(counts[bucket(r['x'])]) for r in rows if not r['y']]
 # Development-only threshold selection, before any main model outcome.
 # Synthetic balanced negatives are not a deployment prevalence prior.
 grid=[i/100 for i in range(5,100,5)]
 model['threshold']=next(t for t in grid if all(p<t for p in normal))
 model['threshold_selection']={'rule':'smallest 0.05 grid threshold allowing all positive development controls','positive_controls':len(normal),'max_positive_score':max(normal),'not_customer_calibrated':True}
 return model

def logistic(w,x):return 1/(1+math.exp(-max(-30,min(30,sum(a*b for a,b in zip(w,x))))))

class Control:
 def __init__(self,arm,model):self.arm=arm;self.model=copy.deepcopy(model);self.updates=[]
 def prediction(self,x):
  a,b=self.model['counts'].get(bucket(x),self.model['global']);return a/(a+b)
 def decide(self,task,state,action):
  from .baselines import predict
  x=features(task,state,action);p=self.prediction(x)
  artifact={'features':x,'risk_probability':p,'baseline_beta':self.model['global'][0]/sum(self.model['global']),
   'baseline_lr':logistic(self.model['lr_weights'],x),'baseline_gbdt':predict(self.model['gbdt'],x),'model_sha256':sha(self.model),'past_updates':len(self.updates)}
  if action['tool'] in ['read','finish','escalate']:return 'ALLOW',artifact
  if self.arm=='B2':
   allow=state['cash_exposure']+action['amount']<=task['cumulative_limit'] and not any(e['tool']==action['tool'] for e in state['journal'])
  elif self.arm in ['B3','B4']:allow=p<self.model['threshold']
  else:allow=True
  return 'ALLOW' if allow else 'BLOCK',artifact
 def observe(self,x,verified_bad,receipt_sha):
  if self.arm!='B4':return
  b=bucket(x)
  if b not in self.model['counts']:self.model['counts'][b]=copy.deepcopy(self.model['global'])
  self.model['counts'][b][int(not verified_bad)]+=1
  self.model['global'][int(not verified_bad)]+=1
  self.updates.append({'receipt_sha256':receipt_sha,'label':int(verified_bad)})
