"""Reproducible offline policy comparison. No model/API called; no bank transfers.

Policies are explicit hand-coded proxies. In particular the heuristic baseline is
NOT an LLM; ap2_inspired is NOT the AP2 protocol implementation.
"""
from __future__ import annotations
import csv, hashlib, io, json, statistics, time
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from .corpus import ROOT,write_corpus
from ..bpce import assess_injection,policy_for_case

POLICIES=['heuristic_assistant_proxy','tool_agent_proxy','static_approval_proxy',
          'ap2_inspired_proxy','bpce_core_proxy',
          'bpce_without_provenance','bpce_without_scope_binding','bpce_without_injection_scan']

def checks(c):
    inv=c['invoice'];q=c['quote']
    return {
      'complete':all(inv.get(k) for k in ('institution','amount','currency','beneficiary','account','invoice_id','deadline')) and not c['document_issues'],
      'beneficiary': inv['beneficiary']==c['registry_beneficiary'] and inv['account']==c['registry_account'] and q['beneficiary']==inv['beneficiary'],
      'case_consistency': inv['amount']==c['case_amount'] and inv['currency']==c['case_currency'],
      'quote_consistency': q['amount']==c['case_amount'] and q['currency']==c['case_currency'] and q['provider'] in ('CAMPUS_SIM_A','CAMPUS_SIM_B'),
      'corridor':not policy_for_case(SimpleNamespace(origin_country=c['origin'],destination_country=c['destination'],currency=c['case_currency']))['hard_blocks'],
      'scope': c['live_evidence_version']==q['evidence_version']==c['approved_scope'],
      'fresh': c['quote_not_expired'],
      'consent': c['consent_recorded'],
      'provider': c['provider_readback']=='COMPLETED',
      'retry':c['idempotency_unique'],
      'injection':not assess_injection(c['untrusted_text']),
      'provenance':bool(c['provenance_id']),
    }

def decide(policy,c):
    x=checks(c)
    requirements={
      'heuristic_assistant_proxy':('complete','case_consistency','corridor'),
      'tool_agent_proxy':('complete','case_consistency','corridor','beneficiary'),
      'static_approval_proxy':('complete','case_consistency','corridor','beneficiary','consent','fresh'),
      'ap2_inspired_proxy':('complete','case_consistency','corridor','beneficiary','consent','fresh','quote_consistency','scope'),
      'bpce_core_proxy': tuple(x.keys()),
      'bpce_without_provenance':tuple(v for v in x if v!='provenance'),
      'bpce_without_scope_binding':tuple(v for v in x if v!='scope'),
      'bpce_without_injection_scan':tuple(v for v in x if v!='injection'),
    }
    if policy not in requirements:raise ValueError('Unrecognized isolated evaluation policy')
    failed=[name for name in requirements[policy] if not x[name]]
    return {'completed':not failed,'failed_checks':failed,'checks':x}

def fraction(a,b):return round(a/b,6) if b else None

def metrics(rows,latencies):
    legit=[r for r in rows if r['safe_to_complete']]
    unsafe=[r for r in rows if not r['safe_to_complete']]
    TP=sum(r['completed'] and not r['safe_to_complete'] for r in rows) # unsafe acceptance
    FP=sum(not r['completed'] and r['safe_to_complete'] for r in rows) # false rejection
    TN=sum(not r['completed'] and not r['safe_to_complete'] for r in rows)
    inv=[r for r in rows if r['is_injection']]
    drift=[r for r in rows if r['requires_reapproval']]
    p95=sorted(latencies)[max(0, int(len(latencies)*.95)-1)] if latencies else None
    return {'samples':len(rows),'legitimate_cases':len(legit),'unsafe_cases':len(unsafe),
       'legitimate_completion_rate':fraction(sum(r['completed'] for r in legit),len(legit)),
       'unsafe_acceptance_rate':fraction(TP,len(unsafe)),
       'unsafe_acceptances':TP,'false_rejection_rate':fraction(FP,len(legit)),
       'precision_of_blocking':fraction(TN,TN+FP),
       'recall_of_blocking':fraction(TN,len(unsafe)),
       'blocking_f1':fraction(2*TN,2*TN+FP+TP),
       'prompt_injection_acceptance_rate':fraction(sum(r['completed'] for r in inv),len(inv)),
       'approval_drift_rejection_rate':fraction(sum(not r['completed'] for r in drift),len(drift)),
       'p50_policy_microseconds':round(statistics.median(latencies),3) if latencies else None,
       'p95_policy_microseconds':round(p95,3) if p95 is not None else None,
       'cost_usd':None,'token_usage':None}

def run(split='holdout',out=None,record_traces=True):
    if split not in ('holdout','development','all'):raise ValueError('split must be holdout/development/all')
    if not (ROOT/'cases.jsonl').exists():write_corpus()
    cases=[json.loads(line) for line in (ROOT/'cases.jsonl').read_text().splitlines()]
    labels={l['case_id']:l for l in map(json.loads,(ROOT/'labels.jsonl').read_text().splitlines())}
    cases=[c for c in cases if split=='all' or c['split']==split]
    assert len({c['case_id'] for c in cases})==len(cases)
    summary={};traces=[]
    for name in POLICIES:
        rows=[];lat=[]
        for c in cases:
            tick=time.perf_counter_ns()
            result=decide(name,c)
            lat.append((time.perf_counter_ns()-tick)/1000)
            truth=labels[c['case_id']]
            row={'case_id':c['case_id'],'category':truth['failure_family'],
                 'safe_to_complete':truth['safe_to_complete'],'is_injection':truth['is_injection'],
                 'requires_reapproval':truth['requires_reapproval'],
                 'completed':result['completed'],'failed_checks':result['failed_checks']}
            rows.append(row)
            if record_traces:traces.append({'policy':name,**row})
        summary[name]=metrics(rows,lat)
    result={'benchmark':'StuPay-IntegrityBench V4.1','evaluation_kind':'OFFLINE_SYNTHETIC_HAND_CODED_POLICY_PROXY',
       'split':split,'cases':len(cases),'policies':summary,
       'notice':'No real LLM, live payment, real fraud case, provider or actual AP2 implementation evaluated.',
       'timing_notice':'Microbenchmark timing includes Python policy checks only; not API or payment latency.',
       'interpretation':'This measures constructed synthetic rule-family outcomes, NOT real-world predictive accuracy.'}
    if out:
        out=Path(out);out.mkdir(parents=True,exist_ok=True)
        (out/f'{split}_results.json').write_text(json.dumps(result,indent=2)+'\n')
        if record_traces:
            with (out/f'{split}_traces.csv').open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=['policy','case_id','category','safe_to_complete','is_injection','requires_reapproval','completed','failed_checks'])
                w.writeheader()
                for r in traces:w.writerow({**r,'failed_checks':';'.join(r['failed_checks'])})
    return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--split',choices=['holdout','development','all'],default='holdout');p.add_argument('--out',default='benchmarks/results');a=p.parse_args()
    print(json.dumps(run(a.split,a.out),indent=2))
