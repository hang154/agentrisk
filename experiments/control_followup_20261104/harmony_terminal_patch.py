"""Owned-server parser repair: only a redundant return after a completed final JSON.

No token-generation setting changes. Generated token IDs, original parser failure
and recovery result are retained. Other malformed output still raises.
"""
import hashlib,json,os,pathlib,time,uuid

def install():
 from openai_harmony import HarmonyError
 from vllm.parser.harmony import HarmonyParser
 original=HarmonyParser.parse
 def parse(self,model_output,request,enable_auto_tools=False,model_output_token_ids=()):
  ids=list(model_output_token_ids)
  try:return original(self,model_output,request,enable_auto_tools,ids)
  except HarmonyError as error:
   record={'epoch':time.time(),'original_error':str(error),'token_ids':ids,'request':request.model_dump(mode='json'),'recovery':'REJECTED'}
   directory=pathlib.Path(os.environ['AGENTRISK_PARSER_EVIDENCE']);directory.mkdir(parents=True,exist_ok=True);dest=directory/(str(time.time_ns())+'-'+uuid.uuid4().hex+'.json')
   try:
    if str(error)!='Unexpected token 200002 while expecting start token 200006' or ids[-2:]!=[200007,200002]:raise error
    self._parser=None;self._num_processed_messages=0;self._current_message_tokens.clear()
    result=original(self,model_output,request,enable_auto_tools,ids[:-1])
    reasoning,content,tools=result
    try:decoded=json.loads(content) if isinstance(content,str) else None
    except (ValueError,TypeError):raise error
    if tools or not isinstance(decoded,dict):raise error
    record['recovery']='REMOVED_REDUNDANT_TERMINAL_AFTER_COMPLETE_FINAL_JSON';record['content']=content;record['reasoning']=reasoning
    return result
   finally:
    with dest.open('x') as f:json.dump(record,f,ensure_ascii=False);f.flush();os.fsync(f.fileno())
 HarmonyParser.parse=parse
 return original

def main():
 install()
 import runpy,sys
 sys.argv=['vllm.entrypoints.openai.api_server']+sys.argv[1:]
 runpy.run_module('vllm.entrypoints.openai.api_server',run_name='__main__')
if __name__=='__main__':main()
