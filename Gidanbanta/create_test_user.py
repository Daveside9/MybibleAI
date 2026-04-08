#!/usr/bin/env python3
"""
Create a test user for testing fantasy team creation
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import date
from backend.app.core.database import get_db
from backend.app.models.user import User, UserRole, KYCStatus
from backend.app.models.wallet import Wallet
from backend.app.core.security import get_password_hash

def create_test_user():
    """Create a test user"""
    db = next(get_db())
    
    # Check if test user already exists
    existing_user = db.query(User).filter(User.email == "test@example.com").first()
    if existing_user:
        print(f"Test user already exists: {existing_user.username}")
        return existing_user
    
    # Create test user
    test_user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        date_of_birth=date(1990, 1, 1),
        role=UserRole.USER,
        kyc_status=KYCStatus.VERIFIED
    )
    
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    
    # Create wallet for test user
    wallet = Wallet(user_id=test_user.id)
    db.add(wallet)
    db.commit()
    
    print(f"Created test user: {test_user.username} (ID: {test_user.id})")
    return test_user

if __name__ == "__main__":
    create_test_user()