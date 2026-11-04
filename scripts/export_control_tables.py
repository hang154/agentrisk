#!/usr/bin/env python3
"""Build follow-up outcome tables and measured runtime from restored raw evidence."""
import argparse,csv,hashlib,json,pathlib

def export(root,out):
 root=pathlib.Path(root);out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True)
 load=lambda p:json.loads(p.read_text());metrics={}
 for folder,sub,filename in [('organizations_continuation','teams','organization_outcomes.csv'),('components_schema_v2','trades','component_outcomes.csv')]:
  flat=[]
  for path in sorted((root/folder/sub).glob('*.json')):
   r=load(path)
   if r.get('pilot') or r.get('job',{}).get('seed')==7000:continue
   if sub=='teams':x=dict(id=r['id'],**r['job'],**r['score'])
   else:x=dict(id=r['id'],family=r['family'],seed=r['seed'],sequence=r['sequence'],**r['arm'],mode=r['selected']['mode'],grant=r['selected']['limit'],selected_supplier=r['selected']['candidate'],**r['outcome'],buyer_net=r['buyer_net'],format_errors=r['format_errors'])
   x.update(status=r['status'],api_calls=len(r['calls']),api_tokens=sum(c['usage']['total_tokens'] for c in r['calls']),output_tokens=r['output_tokens'],source_sha256=hashlib.sha256(path.read_bytes()).hexdigest());flat.append(x)
  with (out/filename).open('w') as f:
   w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
  metrics[folder]={'main_rows':len(flat),'api_calls':sum(x['api_calls'] for x in flat),'api_tokens':sum(x['api_tokens'] for x in flat),'output_tokens':sum(x['output_tokens'] for x in flat)}
 c=metrics['components_schema_v2'];secs=load(root/'components_schema_v2/COMPLETE.json')['result']['seconds']
 c.update(main_seconds=secs,trades_per_minute=c['main_rows']/secs*60,api_tokens_per_second=c['api_tokens']/secs,output_tokens_per_second=c['output_tokens']/secs,unknown=sum(x['status']=='UNKNOWN' for x in flat),format_failures=sum(x['format_errors'] for x in flat),hardware_ceiling_claim=False)
 (out/'RUNTIME_ACCOUNTING.json').write_text(json.dumps(metrics,indent=2))
 return metrics

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--evidence',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 print(json.dumps(export(a.evidence,a.output),indent=2))
