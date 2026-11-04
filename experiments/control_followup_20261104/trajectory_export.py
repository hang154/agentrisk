"""ControlArena directory-writer interchange; no native Inspect/plugin claim."""
import json,pathlib
from experiments.control_study_202611.common import file_sha,freeze
FIELDS={'rating','notes','desc','other','raw_state','metadata','scores','models','system_messages'}
SOURCE='https://github.com/UKGovernmentBEIS/control-arena/blob/eb1494f042d0d587e3a2c3c88fc5416d1d8edc02/control_arena/export/writers/directory.py'
def export(root,destination):
 root=pathlib.Path(root);out=pathlib.Path(destination);out.mkdir(parents=True,exist_ok=True);load=lambda p:json.loads(p.read_text());entries=[];tools={};n=0
 paths=sorted((root/'teams').glob('*.json')) if (root/'teams').exists() else sorted((root/'trades').glob('*.json'))
 for p in paths:
  r=load(p)
  if r.get('pilot') or r.get('job',{}).get('seed')==7000:continue
  messages=[];segments=[];systems=[]
  for c in r['calls']:
   d=root/'raw'/c['id'];q=load(d/'request.json');response=load(d/'response.raw');assert file_sha(d/'request.json')==c['request_sha256'] and file_sha(d/'response.raw')==c['raw_sha256'];start=len(messages)
   for msg in q['messages']:
    if msg['role']=='system':systems.append(msg)
    else:messages.append(msg)
   messages.append({'role':'assistant','content':response['choices'][0]['message']['content']})
   segments.append({'request_id':c['id'],'message_range':[start,len(messages)],'request_sha256':c['request_sha256'],'raw_sha256':c['raw_sha256'],'usage':c['usage']});n+=1
   sch=q['response_format']['json_schema']['schema'];key=json.dumps(sch,sort_keys=True);tools[key]={'name':c['role'],'description':'Constrained JSON action; host execution boundary is separately recorded.','input_schema':sch}
  score=r.get('score',r.get('outcome'));unsafe=score.get('unsafe',score.get('material'));known=score['known'];rating=('unsafe' if unsafe else 'safe') if known and unsafe is not None else None
  entry={'rating':rating,'notes':'Each request segment is a separate actual model context. Repeated context is retained. State/scorer fields are post-action metadata, never injected as prior actor evidence.','desc':r['id'],'other':'','raw_state':json.dumps(messages,ensure_ascii=False),'metadata':{'source_result_sha256':file_sha(p),'native_result':str(p.relative_to(root)),'request_segments':segments,'job':r.get('job',r.get('arm')),'tool_receipts':r.get('events',r.get('transaction')),'adapter':'agentrisk-directory-interchange-v1'},'scores':score,'models':[],'system_messages':systems}
  assert set(entry)==FIELDS;assert all(x['role'] in ['user','assistant'] and isinstance(x['content'],str) for x in json.loads(entry['raw_state']));entries.append(entry)
 with (out/'trajectory.jsonl').open('x') as f:
  for e in entries:f.write(json.dumps(e,ensure_ascii=False)+'\n')
 freeze(out/'tools.json',list(tools.values()));freeze(out/'metadata.json',{'format':'ControlArena directory writer field contract / OpenAI text message representation','reference_source':SOURCE,'native_inspect_eval':False,'native_controlarena_plugin_installed':False,'episodes':len(entries),'raw_calls':n,'model':'openai/gpt-oss-20b','unknown_rating_is_null':True})
 result={'pass':True,'episodes':len(entries),'raw_calls':n,'trajectory_sha256':file_sha(out/'trajectory.jsonl'),'directory_field_contract':sorted(FIELDS),'claim':'export interchange validated, not execution by native ControlArena'};freeze(out/'EXPORT_VALIDATION.json',result);return result
if __name__=='__main__':
 import sys;print(json.dumps(export(sys.argv[1],sys.argv[2])))
