"""Explicit external boundary. No network or money movement is implemented here.

The normal simulator never imports an external transfer adapter. Credentials and
separate user authorization are prerequisites to any future sandbox connector.
"""
from dataclasses import dataclass
from typing import Protocol

class SandboxProvider(Protocol):
    def capabilities(self)->dict: ...
    def read_transfer(self, reference:str)->dict: ...

class ExternalSandboxBlocked(RuntimeError):pass

@dataclass(frozen=True)
class BlockedSandboxAdapter:
    provider:str
    base_url:str
    def capabilities(self):
        return {'provider':self.provider,'environment':'EXTERNAL_SANDBOX',
            'status':'BLOCKED_BY_EXTERNAL_CREDENTIALS_AND_SEPARATE_AUTHORIZATION',
            'connected':False,'network_calls_implemented':False,'real_payments_enabled':False}
    def read_transfer(self, reference:str):
        raise ExternalSandboxBlocked('No external provider response exists; connection is blocked')

WISE_SANDBOX=BlockedSandboxAdapter('Wise Sandbox V2','https://api.wise-sandbox.com')
AIRWALLEX_SANDBOX=BlockedSandboxAdapter('Airwallex sandbox','https://api.sandbox.airwallex.com')
