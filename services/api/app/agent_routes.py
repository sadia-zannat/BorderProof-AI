"""Authenticated, CSRF-protected, persisted chat turns; agent can only inspect data."""
from __future__ import annotations
from .timeutils import iso_utc
import json,os
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from .db import db_session
from .models import User,AgentConversation
from .finance import owned_case
from .security import current_user,require_mutation_roles
from .local_agent import configuration,run_agent,TOOL_NAMES
from .audit import append_event

router=APIRouter(prefix='/api/v1',tags=['V5.1 Local Autonomous Agent'])
class AgentChatInput(BaseModel):
    message:str=Field(min_length=2,max_length=1200)
    conversation_id:str|None=Field(default=None,pattern=r'^[0-9a-f]{32}$')

def _owned_chat(db:Session,cid:str,user_id:str)->AgentConversation:
    item=db.get(AgentConversation,cid)
    if not item or item.owner_id!=user_id:raise HTTPException(404,'Agent conversation not found')
    owned_case(db,item.case_id,user_id)
    return item

@router.get('/agent/capabilities')
def capabilities(user:User=Depends(current_user)):
    if os.getenv('OLLAMA_ENABLED','1')!='1':
        return {'provider':'OLLAMA_LOCAL_API','model':os.getenv('OLLAMA_MODEL','qwen3:4b'),'status':'DISABLED',
            'model_loaded_not_verified':True,'read_only_tools':list(TOOL_NAMES),'can_execute':False,'can_authorize':False}
    try:cfg=configuration()
    except RuntimeError as exc:raise HTTPException(503,str(exc)) from exc
    return {'provider':'OLLAMA_LOCAL_API','model':cfg['model'],'base_url':cfg['url'],
        'model_loaded_not_verified':True,'read_only_tools':list(TOOL_NAMES),
        'can_execute':False,'can_authorize':False,'live_model_test_required':True,
        'warning':'Real Qwen inference requires Ollama running locally. No fallback is mislabeled as AI.'}

@router.get('/agent/conversations')
def list_conversations(user:User=Depends(current_user),db:Session=Depends(db_session)):
    if user.role!='student':raise HTTPException(403,'Student only')
    items=db.scalars(select(AgentConversation).where(AgentConversation.owner_id==user.id).order_by(AgentConversation.created_at.desc()).limit(30)).all()
    return {'items':[{'id':x.id,'case_id':x.case_id,'updated_at':iso_utc(x.updated_at)} for x in items]}

@router.get('/agent/conversations/{conversation_id}')
def get_conversation(conversation_id:str,user:User=Depends(current_user),db:Session=Depends(db_session)):
    if user.role!='student':raise HTTPException(403,'Student only')
    item=_owned_chat(db,conversation_id,user.id)
    return {'id':item.id,'case_id':item.case_id,'messages':json.loads(item.messages_json),
            'last_tool_trace':json.loads(item.last_tool_trace_json)}

@router.post('/cases/{case_id}/agent/chat')
def chat(case_id:str, inp:AgentChatInput, user:User=Depends(require_mutation_roles('student')),db:Session=Depends(db_session)):
    owned_case(db,case_id,user.id)
    if not inp.message.strip():raise HTTPException(422,'Question must not be blank')
    item=_owned_chat(db,inp.conversation_id,user.id) if inp.conversation_id else None
    if item and item.case_id!=case_id:raise HTTPException(404,'Agent conversation not found')
    history=json.loads(item.messages_json) if item else []
    try:result=run_agent(db,case_id,user.id,inp.message,history)
    except HTTPException as exc:
        append_event(db,user.id,'LOCAL_AGENT_FAILED','case',case_id,
            {'http_status':exc.status_code,'model_response_fabricated':False,'financial_action':False})
        db.commit()
        raise
    if item is None:
        item=AgentConversation(owner_id=user.id,case_id=case_id,messages_json='[]',last_tool_trace_json='[]')
        db.add(item);db.flush()
    history=(history+[{'role':'user','content':inp.message},{'role':'assistant','content':result['message']}])[-24:]
    item.messages_json=json.dumps(history,ensure_ascii=False)
    item.last_tool_trace_json=json.dumps(result['tool_trace'],ensure_ascii=False)
    from datetime import datetime,timezone
    item.updated_at=datetime.now(timezone.utc)
    append_event(db,user.id,'LOCAL_AGENT_READ_ONLY','agent_conversation',item.id,
        {'case_id':case_id,'tool_names':[x['name'] for x in result['tool_trace']],
         'tool_count':result['tool_count'],'real_payment':False})
    db.commit()
    return {'conversation_id':item.id,**result}
