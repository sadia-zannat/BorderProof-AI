"""Research module does not mutate production transactions; fixture labels are separate."""
import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from benchmarks.stupay_integritybench.corpus import GROUPS,generate,make_case,write_corpus,ROOT
from benchmarks.stupay_integritybench.evaluator import run,decide,POLICIES,checks
from services.api.app.main import app


def test_corpus_shape_distribution_and_labels():
    cases,labels=generate()
    assert len(cases)==len(labels)==300
    assert len({c['case_id'] for c in cases})==300
    assert {g:sum(l['failure_family']==('none' if g=='legitimate' else g) for l in labels) for g,n in GROUPS} ==dict(GROUPS)
    assert sum(c['split']=='holdout' for c in cases)==60
    assert sum(c['split']=='development' for c in cases)==240
    assert all(l['case_id']==c['case_id'] for c,l in zip(cases,labels))
    assert not any('safe_to_complete' in c for c in cases)


def test_frozen_dataset_matches_generator():
    cases,labels=generate()
    assert [json.loads(x) for x in (ROOT/'cases.jsonl').read_text(encoding='utf-8').splitlines()]==cases
    assert [json.loads(x) for x in (ROOT/'labels.jsonl').read_text(encoding='utf-8').splitlines()]==labels
    from hashlib import sha256
    meta=json.loads((ROOT/'metadata.json').read_text(encoding='utf-8'))
    assert all(meta['sha256'][name]==sha256((ROOT/name).read_bytes()).hexdigest() for name in ('cases.jsonl','labels.jsonl'))


def test_repeatable_deterministic_predictions():
    cases,_=generate()
    for c in cases:
        for p in POLICIES:
            assert decide(p,c)==decide(p,c)


def test_security_ablations_honest_gaps():
    report=run('holdout')
    assert report['cases']==60
    p=report['policies']
    assert p['bpce_core_proxy']['unsafe_acceptances']>0, 'Do not pretend regex catches all attacks'
    assert p['bpce_core_proxy']['false_rejection_rate']>0, 'Allow honest false positive measurement'
    assert p['bpce_without_provenance']['unsafe_acceptances'] > p['bpce_core_proxy']['unsafe_acceptances']
    assert p['bpce_without_scope_binding']['unsafe_acceptances'] > p['bpce_core_proxy']['unsafe_acceptances']
    assert p['bpce_without_injection_scan']['unsafe_acceptances'] > p['bpce_core_proxy']['unsafe_acceptances']
    assert p['bpce_core_proxy']['unsafe_acceptance_rate'] < p['heuristic_assistant_proxy']['unsafe_acceptance_rate']


def test_replay_no_payment_mutation_and_auth_isolation():
    # Research results should never be available to unauthenticated clients.
    with TestClient(app) as client:
        for url in ('/api/v1/research/summary','/api/v1/research/cases','/api/v1/research/replay/LEGITIMATE-000'):
            assert client.get(url).status_code==401


def test_invalid_policy_rejected_by_function():
    c,_=make_case('legitimate',0)
    with pytest.raises(ValueError):decide('disabled_security_in_app',c)


def test_json_results_correspond_to_actual_run():
    frozen=json.loads((Path('benchmarks/results/holdout_results.json')).read_text(encoding='utf-8'))
    fresh=run('holdout')
    for policy in POLICIES:
        # Wall timings naturally fluctuate; assert invariant measured counts/rates.
        for field in ('samples','legitimate_completion_rate','unsafe_acceptance_rate','unsafe_acceptances',
                      'false_rejection_rate','blocking_f1','prompt_injection_acceptance_rate'):
            assert frozen['policies'][policy][field]==fresh['policies'][policy][field]


def test_study_inputs_are_synthetic():
    cases,_=generate()
    assert all(c['invoice']['institution'].startswith('SYNTHETIC UNIVERSITY') for c in cases)
    assert not any('password' in c or 'passport' in c or 'api_key' in c for c in cases)

def test_authenticated_research_endpoints_and_replay(client):
    from .conftest import sign_in
    sign_in(client,'student')
    data=client.get('/api/v1/research/summary');assert data.status_code==200,data.text
    assert data.json()['results']['cases']==60
    assert data.json()['metadata']['cases']==300
    listing=client.get('/api/v1/research/cases',params={'category':'prompt_injection','split':'holdout'})
    assert listing.status_code==200
    assert listing.json()['total']==10
    case_id=listing.json()['items'][0]['case_id']
    info=client.get('/api/v1/research/replay/'+case_id)
    assert info.status_code==200
    assert info.json()['source_type']=='ORIGINAL_SYNTHETIC_FIXTURE'
    assert len(info.json()['checks'])>=10
    # Replay is read-only and cannot create payment cases, approvals or transfers.
    from app.db import SessionLocal
    from app.models import PaymentCase,PaymentApproval,SandboxTransfer
    from sqlalchemy import select
    with SessionLocal() as db:
        assert not db.scalars(select(PaymentCase)).all()
        assert not db.scalars(select(PaymentApproval)).all()
        assert not db.scalars(select(SandboxTransfer)).all()


def test_replay_rejects_invalid_policy_unknown_case_and_pagination(client):
    from .conftest import sign_in
    sign_in(client)
    assert client.get('/api/v1/research/replay/LEGITIMATE-000?policy=undeclared').status_code==422
    assert client.get('/api/v1/research/replay/MISSING-999').status_code==404
    assert client.get('/api/v1/research/cases?limit=1000').status_code==422
    assert client.get('/api/v1/research/cases?category=unknown').status_code==422
