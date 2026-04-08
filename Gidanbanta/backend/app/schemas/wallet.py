"""
Wallet Schemas
Request/Response models for wallet operations
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class WalletResponse(BaseModel):
    id: int
    user_id: int
    balance: float
    deposited_amount: float
    winnings_amount: float
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    type: str
    amount: float = Field(..., gt=0)
    provider: Optional[str] = None
    match_id: Optional[int] = None
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    type: str
    amount: float
    status: str
    provider: Optional[str]
    description: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class TopUpRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Amount in Naira")
    provider: str = Field(..., description="Payment provider: opay, palmpay, moniepoint")

class WithdrawRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Amount to withdraw")
    bank_account: str
    bank_code: str
