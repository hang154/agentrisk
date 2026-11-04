import bisect,itertools,math,random

def mean(x):return sum(x)/len(x) if x else None
def quantile(x,p):
 x=sorted(x);v=(len(x)-1)*p;i=int(v);return x[i]+(x[min(i+1,len(x)-1)]-x[i])*(v-i)
def signed_sums(x):
 s=[0.]
 for v in x:s=[a-v for a in s]+[a+v for a in s]
 return s

def cluster_effect(groups):
 vals=[mean(v) for _,v in sorted(groups.items()) if v];n=len(vals)
 if not n:return dict(effect=None,clusters=0,pairs=0)
 rng=random.Random(20261104);draws=[mean(rng.choices(vals,k=n)) for _ in range(5000)];obs=abs(sum(vals));left=signed_sums(vals[:n//2]);right=sorted(signed_sums(vals[n//2:]));tol=1e-10
 # Exact paired sign-flip, meet in the middle; practical through 40 clusters.
 if n<=32:
  if obs<=tol:p=1.
  else:
   count=sum(bisect.bisect_right(right,-obs-a+tol)+len(right)-bisect.bisect_left(right,obs-a-tol) for a in left);p=min(1,count/(2**n))
 else:p=None
 return dict(effect=mean(vals),cluster_bootstrap_ci95=[quantile(draws,.025),quantile(draws,.975)],one_sided95_lower=quantile(draws,.05),clusters=n,pairs=sum(map(len,groups.values())),exact_two_sided_signflip_p=p)
def holm(items):
 prev=0;out={};rows=sorted((p,k) for k,p in items.items() if p is not None)
 for i,(p,k) in enumerate(rows):prev=max(prev,min(1,p*(len(rows)-i)));out[k]=prev
 return out

def binary_score(p,y):
 p=min(1-1e-9,max(1e-9,p));return (p-y)**2,-y*math.log(p)-(1-y)*math.log(1-p)
