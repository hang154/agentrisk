"""Sandbox state transitions. This module never calls the scoring oracle."""
import copy,time
from .common import sha

def initial_state():return {'records':{},'journal':[],'cash_exposure':0,'escalated':False}

def hard_gate(task,action):
 if set(action)!={'tool','subject','value','amount','reference','reason'}:return 'DENIED_SCHEMA'
 if type(action['amount']) is not int or action['amount']<0:return 'DENIED_AMOUNT_TYPE'
 if not all(isinstance(action[k],str) for k in ['tool','subject','value','reference','reason']):return 'DENIED_TYPE'
 if action['tool'] in ['read','finish','escalate']:return 'ALLOW'
 if action['tool'] not in task['tool_scope']:return 'DENIED_TOOL_SCOPE'
 if action['subject']!=task['subject']:return 'DENIED_SUBJECT_ACL'
 if action['reference']!=task['contract_id']:return 'DENIED_AUTHORIZATION_REFERENCE'
 if action['amount']>task['per_action_limit']:return 'DENIED_PER_ACTION_LIMIT'
 return 'ALLOW'

def execute(task,state,action,additional='ALLOW'):
 before=copy.deepcopy(state);gate=hard_gate(task,action)
 if gate=='ALLOW' and additional!='ALLOW':gate='DENIED_ADDITIONAL_CONTROL'
 tool=action['tool'];executed=False
 if gate=='ALLOW':
  if tool=='escalate':state['escalated']=True
  elif tool not in ['read','finish']:
   executed=True
   entry={'tool':tool,'subject':action['subject'],'value':action['value'],'amount':action['amount'],'reference':action['reference'],'index':len(state['journal'])}
   state['journal'].append(copy.deepcopy(entry));state['records'][tool]=copy.deepcopy(entry)
   state['cash_exposure']+=action['amount']
 receipt={'sequence':len(before['journal']),'execution_epoch':time.time(),'proposal':copy.deepcopy(action),'hard_gate':hard_gate(task,action),'decision':gate,'executed':executed,'before':before,'after':copy.deepcopy(state)}
 receipt['sha256']=sha(receipt)
 observation={'decision':gate,'executed':executed,'receipt_sha256':receipt['sha256'],'state':copy.deepcopy(state)}
 return observation,receipt

def verify_receipts(initial,events,final):
 state=copy.deepcopy(initial)
 for i,e in enumerate(events):
  receipt=e['receipt'];check={k:v for k,v in receipt.items() if k!='sha256'}
  if sha(check)!=receipt['sha256']:raise ValueError('RECEIPT_MUTATED')
  if receipt['before']!=state:raise ValueError('STATE_CHAIN_BROKEN')
  if e['pre_state_sha256']!=sha(state):raise ValueError('PRE_ACTION_STATE_MISMATCH')
  if not receipt['executed'] and receipt['proposal']['tool']!='escalate' and receipt['before']!=receipt['after']:raise ValueError('BLOCKED_STATE_CHANGED')
  state=receipt['after']
 if state!=final:raise ValueError('FINAL_STATE_MISMATCH')
 return True
