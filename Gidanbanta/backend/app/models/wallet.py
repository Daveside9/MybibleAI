"""
Wallet & Transaction Models
Handles virtual credits and transactions
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base

class TransactionType(str, enum.Enum):
    DEPOSIT = "deposit"           # User tops up
    WITHDRAWAL = "withdrawal"     # User withdraws winnings
    CHAT_UNLOCK = "chat_unlock"   # Per-match chat access
    FANTASY_ENTRY = "fantasy_entry"  # Fantasy contest entry
    FANTASY_WIN = "fantasy_win"   # Fantasy prize
    REFUND = "refund"             # Refund for cancelled match
    ADMIN_CREDIT = "admin_credit" # Admin adjustment
    ADMIN_DEBIT = "admin_debit"   # Admin adjustment

class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Wallet(Base):
    __tablename__ = "wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Balance (in credits, 1 credit = 1 Naira)
    balance = Column(Float, default=0.0, nullable=False)
    deposited_amount = Column(Float, default=0.0, nullable=False)  # Total deposited (cannot withdraw)
    winnings_amount = Column(Float, default=0.0, nullable=False)   # Winnings (can withdraw)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="wallet")
    
    def __repr__(self):
        return f"<Wallet user_id={self.user_id} balance={self.balance}>"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Transaction details
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING, nullable=False)
    
    # Payment provider details (for deposits/withdrawals)
    provider = Column(String, nullable=True)  # opay, palmpay, moniepoint
    provider_reference = Column(String, nullable=True)
    provider_response = Column(String, nullable=True)
    
    # Related entities
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=True)
    fantasy_contest_id = Column(Integer, nullable=True)
    
    # Metadata
    description = Column(String, nullable=True)
    meta_data = Column(String, nullable=True)  # JSON string for additional data
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    match = relationship("Match", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction {self.type} {self.amount} {self.status}>"
