"""Read-only public references. Never settlement, legal eligibility or payee ownership."""
from datetime import datetime, timezone, date
from decimal import Decimal
import hashlib
import json
import httpx
from fastapi import HTTPException

FX_URL='https://api.frankfurter.dev/v1/latest'

def fetch_reference_fx(base='EUR'):
    if base not in ('EUR','USD','GBP','CAD'):raise HTTPException(422,'Unsupported base currency')
    observed=datetime.now(timezone.utc).isoformat()
    try:
        response=httpx.get(FX_URL,params={'base':base},timeout=8,follow_redirects=False)
        response.raise_for_status()
        body=json.loads(response.text,parse_float=Decimal)
        if body['base']!=base or not body['rates']:raise ValueError('Invalid reference response')
        effective=date.fromisoformat(body['date'])
        if effective>datetime.now(timezone.utc).date():raise ValueError('Future rate date')
        rates={}
        for currency,value in body['rates'].items():
            amount=Decimal(str(value))
            if len(currency)!=3 or not currency.isalpha() or not amount.is_finite() or amount<=0:raise ValueError('Invalid reference rate')
            rates[currency]=str(amount)
        return {'status':'REFERENCE_ONLY','base':base,'date':body['date'],'rates':rates,
            'source_url':FX_URL+'?base='+base,'retrieved_at_utc':observed,
            'published_effective_date':body['date'],'response_sha256':hashlib.sha256(response.content).hexdigest(),
            'cache_status':'FRESH_HTTP_RESPONSE_NO_APP_CACHE','fallback_used':False,
            'precision':'Provider decimal representation retained as strings; daily reference, not executable pricing',
            'source':'Frankfurter v1 / ECB daily published reference data',
            'use_limits':'Public reference only. Provider software license does not establish ownership of underlying rate data; see source terms.',
            'terms_url':'https://frankfurter.dev/','verified_execution_quote':False}
    except (httpx.HTTPError,ValueError,KeyError,TypeError,ArithmeticError,ImportError):
        raise HTTPException(503,'Public FX reference UNAVAILABLE; no cached or invented rate substituted')

REFERENCE_SOURCES=[
    {'id':'ecb','url':'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html','scope':'Daily FX reference; not executable quote'},
    {'id':'ucl','url':'https://www.ucl.ac.uk/students/fees-and-funding/pay-your-fees','scope':'University payment guidance only; no bank beneficiary attestation'},
    {'id':'world_bank','url':'https://remittanceprices.worldbank.org/','scope':'Historical corridor cost research; not a student-specific live quote'},
    {'id':'bangladesh_bank','url':'https://www.bb.org.bd/','scope':'Official central bank material; specific student eligibility has NOT been verified'},
]
