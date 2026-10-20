"""Read-only V4 SYNTHETIC study endpoints. Research policy executions are isolated.
No route here creates payment cases, approval tokens, or transfers.
"""
from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from .models import User
from .security import current_user
from .stupay_core.corpus import ROOT, GROUPS
from .stupay_core.evaluator import POLICIES, decide

router=APIRouter(prefix='/api/v1/research',tags=['V4 SYNTHETIC Research (Read-only)'])
RESULTS=Path(__file__).resolve().parents[3]/'benchmarks'/'results'

@lru_cache(maxsize=1)
def fixture_data():
    # Bundled immutable study data; never read user documents or DB transaction state.
    cases=[json.loads(line) for line in (ROOT/'cases.jsonl').read_text(encoding='utf-8').splitlines()]
    labels={r['case_id']:r for r in map(json.loads,(ROOT/'labels.jsonl').read_text(encoding='utf-8').splitlines())}
    if len(cases)!=300 or len(labels)!=300 or len({c['case_id'] for c in cases})!=300:
        raise RuntimeError('Invalid research corpus manifest')
    return cases,labels

@router.get('/summary')
def summary(user:User=Depends(current_user)):
    file=RESULTS/'holdout_results.json'
    if not file.is_file():raise HTTPException(503,'Research results have not been generated')
    return {'results':json.loads(file.read_text(encoding='utf-8')),
            'metadata':json.loads((ROOT/'metadata.json').read_text(encoding='utf-8')),
            'notice':'Evaluation uses 60 stratified holdout SYNTHETIC fixtures and handcrafted proxy policies; zero real transfers.'}

@router.get('/cases')
def list_cases(category:str|None=None,split:str='holdout',offset:int=Query(0,ge=0),limit:int=Query(20,ge=1,le=100),user:User=Depends(current_user)):
    if split not in ('holdout','development','all'):raise HTTPException(422,'Invalid split')
    if category and category not in dict(GROUPS):raise HTTPException(422,'Invalid category')
    cases,labels=fixture_data()
    selected=[c for c in cases if (split=='all' or c['split']==split) and (not category or labels[c['case_id']]['failure_family']==category)]
    return {'total':len(selected),'offset':offset,'limit':limit,'items':[
        {'case_id':c['case_id'],'split':c['split'],'category':labels[c['case_id']]['failure_family'],
         'safe_to_complete':labels[c['case_id']]['safe_to_complete'],
         'destination':c['destination'],'currency':c['case_currency']}
        for c in selected[offset:offset+limit]], 'fixture_type':'SYNTHETIC_ONLY'}

@router.get('/replay/{case_id}')
def replay_case(case_id:str,policy:str='bpce_core_proxy',user:User=Depends(current_user)):
    if policy not in POLICIES:raise HTTPException(422,'Unknown research policy')
    cases,labels=fixture_data()
    case=next((c for c in cases if c['case_id']==case_id),None)
    if case is None:raise HTTPException(404,'Fixture not found')
    result=decide(policy,case)
    nodes=[{'id':name,'passed':passed} for name,passed in result['checks'].items()]
    return {'case_id':case_id,'policy':policy,'split':case['split'],
        'decision':'COMPLETE_SIMULATED' if result['completed'] else 'BLOCK_SIMULATED',
        'ground_truth_safe':labels[case_id]['safe_to_complete'],
        'ground_truth_family':labels[case_id]['failure_family'],
        'failed_checks':result['failed_checks'],'checks':nodes,
        'invoice':case['invoice'],'quote':case['quote'],
        'untrusted_text':case['untrusted_text'],
        'edges':[{'from':'invoice','to':'case_consistency'},
                 {'from':'registry','to':'beneficiary'},
                 {'from':'document','to':'scope'},
                 {'from':'quote','to':'quote_consistency'},
                 {'from':'approval','to':'scope'},
                 {'from':'provider','to':'retry'}],
        'source_type':'ORIGINAL_SYNTHETIC_FIXTURE',
        'warning':'Offline proxy replay; never executed a payment or contacted a bank.'}
