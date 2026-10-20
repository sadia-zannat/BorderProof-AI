"""All response contracts are intentionally explicit; no raw ORM serialization."""
from __future__ import annotations
from decimal import Decimal, InvalidOperation
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Literal
from pydantic import model_validator
from .network_config import REGION_CURRENCIES, CURRENCIES

class LoginIn(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=1, max_length=256)

class RegisterIn(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    email: str = Field(min_length=5,max_length=255,pattern=r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
    name: str = Field(min_length=2,max_length=120)
    password: str = Field(min_length=12,max_length=256)

class ProfileUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    institution: str = Field(max_length=160)
    home_country: str = Field(min_length=2, max_length=64)
    currency: Literal['BDT','CNY','GBP','USD','CAD','EUR','AUD','SGD']

class CaseIn(BaseModel):
    title: str = Field(min_length=3,max_length=160)
    institution: str = Field(min_length=3,max_length=160)
    origin_country: Literal['Bangladesh','China','United Kingdom','United States','Canada','Euro Area','Australia','Singapore']='Bangladesh'
    destination_country: Literal['Bangladesh','China','United Kingdom','United States','Canada','Euro Area','Australia','Singapore']
    amount: str
    currency: Literal['BDT','CNY','GBP','USD','CAD','EUR','AUD','SGD']
    source_currency: Literal['BDT','CNY','GBP','USD','CAD','EUR','AUD','SGD'] | None = None
    destination_currency: Literal['BDT','CNY','GBP','USD','CAD','EUR','AUD','SGD'] | None = None

    @model_validator(mode='after')
    def valid_cross_border(self):
        if self.origin_country==self.destination_country:
            raise ValueError('International payment planning requires different origin and destination')
        if self.source_currency is None:self.source_currency=REGION_CURRENCIES[self.origin_country]
        if self.destination_currency is None:self.destination_currency=REGION_CURRENCIES[self.destination_country]
        return self

    @field_validator('amount')
    @classmethod
    def valid_amount(cls, v):
        try: d = Decimal(v)
        except (InvalidOperation, TypeError): raise ValueError('Invalid monetary amount')
        if not d.is_finite() or d <= 0 or d > Decimal('1000000') or d.as_tuple().exponent < -2:
            raise ValueError('Amount must be positive, <= 1,000,000, with <= 2 decimal places')
        return f'{d:.2f}'
