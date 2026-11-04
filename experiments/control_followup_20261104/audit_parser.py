"""Match scoped Harmony recoveries to the actual wire response and token usage."""
import concurrent.futures,json,pathlib
from experiments.control_study_202611.common import freeze,file_sha

def audit(root,raw_roots,write=True):
 root=pathlib.Path(root);load=lambda p:json.loads(p.read_text());records={}
 for p in (root/'parser_runtime_evidence').glob('*.json'):
  r=load(p);assert r['recovery']=='REMOVED_REDUNDANT_TERMINAL_AFTER_COMPLETE_FINAL_JSON'
  assert r['original_error']=='Unexpected token 200002 while expecting start token 200006' and r['token_ids'][-2:]==[200007,200002] and isinstance(json.loads(r['content']),dict)
  key='chatcmpl-'+r['request']['request_id'];assert key not in records;records[key]=(r,p)
 def one(p):
  z=load(p)
  if z['id'] not in records:return None
  r,path=records[z['id']];q=load(p.parent/'request.json');receipt=load(p.parent/'receipt.json')
  assert z['choices'][0]['message']['content']==r['content'] and z['choices'][0]['finish_reason']=='stop'
  assert z['usage']['completion_tokens']==len(r['token_ids']) and z['usage']==receipt['usage']
  assert file_sha(p)==receipt['raw_sha256'] and file_sha(p.parent/'request.json')==receipt['request_sha256']
  for k in ['model','seed','temperature','top_p','reasoning_effort','max_tokens']:assert q[k]==r['request'][k]
  assert [(x['role'],x['content']) for x in q['messages']]==[(x['role'],x['content']) for x in r['request']['messages']]
  return {'response_id':z['id'],'request_id':p.parent.name,'recovery_sha256':file_sha(path),'raw_sha256':file_sha(p),'generated_tokens':len(r['token_ids']),'reported_completion_tokens':z['usage']['completion_tokens']}
 paths=[p for rr in raw_roots for p in (pathlib.Path(rr)/'raw').glob('*/response.raw')]
 with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:matches=[v for v in pool.map(one,paths) if v]
 assert {r['response_id'] for r in matches}==set(records)
 # Overlapping archived paths are allowed only when the original response is identical.
 by_id={}
 for row in matches:
  if row['response_id'] in by_id:assert row==by_id[row['response_id']]
  by_id[row['response_id']]=row
 result={'pass_gate':True,'recoveries':len(records),'raw_responses_matched':len(by_id),'generation_tokens_unchanged':True,'original_failed_requests_not_converted_to_success':True,'rows':[by_id[k] for k in sorted(by_id)]}
 if write:freeze(root/'PARSER_RECOVERY_AUDIT.json',result)
 return result
if __name__=='__main__':
 import sys;print(json.dumps(audit(sys.argv[1],sys.argv[2:])))
