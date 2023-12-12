from pydantic import BaseModel
from typing import Any


class Address(BaseModel):
    city: Any
    country: str
    line1: Any
    email: str


class BillingDetails(BaseModel):
    address: Address


class GeneratedModel(BaseModel):
    id: str
    object: str
    price: float
    price_str: Any
    billing_details: BillingDetails
