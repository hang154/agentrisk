"""Small reproducible logistic GBDT baseline (Newton trees, depth two).

Uses the same seven observable pre-action inputs and calibration labels as the
AgentRisk Beta-bucket policy. It is not the historical private RiskRank model.
"""
import math
def sigmoid(x):return 1/(1+math.exp(-max(-30,min(30,x))))
def tree_predict(tree,x):
 if 'leaf' in tree:return tree['leaf']
 return tree_predict(tree['left'] if x[tree['feature']]<=tree['threshold'] else tree['right'],x)
def fit_tree(xs,gs,hs,indices,depth):
 g=sum(gs[i] for i in indices);h=sum(hs[i] for i in indices)
 leaf={'leaf':g/(h+1)}
 if depth==0 or len(indices)<4:return leaf
 best=None;gain=0
 for j in range(len(xs[0])):
  vals=sorted({xs[i][j] for i in indices})
  for lo,hi in zip(vals,vals[1:]):
   t=(lo+hi)/2;left=[i for i in indices if xs[i][j]<=t];right=[i for i in indices if xs[i][j]>t]
   if min(len(left),len(right))<2:continue
   gl=sum(gs[i] for i in left);hl=sum(hs[i] for i in left);gr=g-gl;hr=h-hl
   delta=gl*gl/(hl+1)+gr*gr/(hr+1)-g*g/(h+1)
   if delta>gain+1e-12:gain=delta;best=(j,t,left,right)
 if best is None:return leaf
 j,t,l,r=best
 return {'feature':j,'threshold':t,'left':fit_tree(xs,gs,hs,l,depth-1),'right':fit_tree(xs,gs,hs,r,depth-1)}
def fit(rows):
 xs=[r['x'] for r in rows];ys=[r['y'] for r in rows];p=(1+sum(ys))/(2+len(ys));base=math.log(p/(1-p));z=[base]*len(xs);trees=[]
 for _ in range(60):
  ps=[sigmoid(v) for v in z];g=[y-p for y,p in zip(ys,ps)];h=[max(1e-6,p*(1-p)) for p in ps]
  tree=fit_tree(xs,g,h,list(range(len(xs))),2);trees.append(tree)
  z=[v+0.1*tree_predict(tree,x) for v,x in zip(z,xs)]
 return {'algorithm':'logistic_gradient_boosted_trees','depth':2,'estimators':60,'learning_rate':0.1,'l2':1,'base_logit':base,'trees':trees}
def predict(model,x):return sigmoid(model['base_logit']+model['learning_rate']*sum(tree_predict(t,x) for t in model['trees']))
