from __future__ import annotations

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    error: str
    detail: object | str


class CreatePortfolioSchema(BaseModel):
    username: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class BuyTradeSchema(BaseModel):
    portfolio_id: int
    ticker: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)


class SellTradeSchema(BaseModel):
    portfolio_id: int
    ticker: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)


class GrantAccessSchema(BaseModel):
    username: str = Field(..., min_length=1)
    role: str = Field(..., pattern=r"^(viewer|manager)$")


class RevokeAccessSchema(BaseModel):
    username: str = Field(..., min_length=1)
    
from pydantic import BaseModel, Field


class CreateUserSchema(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    firstname: str = Field(min_length=1)
    lastname: str = Field(min_length=1)
    balance: float


class UpdateBalanceSchema(BaseModel):
    username: str = Field(min_length=1)
    new_balance: float