"""
User Model
Handles user accounts, authentication, and KYC
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base

class UserRole(str, enum.Enum):
    SPECTATOR = "spectator"  # Under 18, limited access
    USER = "user"            # Regular user
    PREMIUM = "premium"      # Subscribed user
    MODERATOR = "moderator"  # Content moderator
    ADMIN = "admin"          # Full admin access

class KYCStatus(str, enum.Enum):
    UNVERIFIED = "unverified"
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Profile
    full_name = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=False)
    phone_number = Column(String, nullable=True)
    
    # Status
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    kyc_status = Column(Enum(KYCStatus), default=KYCStatus.UNVERIFIED, nullable=False)
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    wallet = relationship("Wallet", back_populates="user", uselist=False)
    transactions = relationship("Transaction", back_populates="user")
    chat_messages = relationship("ChatMessage", back_populates="user")
    # fantasy_team = relationship("FantasyTeam", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    @property
    def age(self):
        """Calculate user's age"""
        today = datetime.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    @property
    def is_adult(self):
        """Check if user is 18+"""
        return self.age >= 18
    
    @property
    def can_purchase(self):
        """Check if user can make purchases"""
        return self.is_adult and self.kyc_status == KYCStatus.VERIFIED
