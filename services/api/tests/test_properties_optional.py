"""Actual Hypothesis property tests when optional dev dependency is installed.
In no-network execution environments this module is skipped, not reported as passed.
"""
from decimal import Decimal
import pytest
hypothesis=pytest.importorskip('hypothesis',reason='Install requirements-dev.txt for Hypothesis property tests')
from hypothesis import given,settings,strategies as st
from app.finance import as_money
from app.bpce import hash_of,attack_probe

@settings(max_examples=100,deadline=None)
@given(st.decimals(min_value='0.01',max_value='1000000.00',places=2,allow_nan=False,allow_infinity=False))
def test_decimal_money_roundtrip(value):
    actual=Decimal(as_money(value))
    assert actual==value
    assert actual.as_tuple().exponent==-2

@settings(max_examples=100,deadline=None)
@given(st.text(min_size=0,max_size=120),st.integers(min_value=0,max_value=999999))
def test_evidence_hash_deterministic_and_sensitive_to_amount(title,amount):
    original={'case':title,'amount':amount}
    assert hash_of(original)==hash_of({'amount':amount,'case':title})
    assert hash_of(original)!=hash_of({'amount':amount+1,'case':title})

@settings(max_examples=80,deadline=None)
@given(st.text(max_size=300))
def test_untrusted_text_cannot_grant_execution_authority(text):
    result=attack_probe(text)
    assert result['can_execute'] is False
    assert result['can_authorize'] is False
    assert result['can_request_tools'] is False
