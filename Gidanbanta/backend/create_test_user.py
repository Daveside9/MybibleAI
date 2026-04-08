"""
Create Test User Script
Run this to create a test user for fantasy team testing
"""
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole, KYCStatus
from app.models.wallet import Wallet
from datetime import date

def create_test_user():
    db = SessionLocal()
    
    # Check if test user already exists
    existing_user = db.query(User).filter(User.email == "test@example.com").first()
    if existing_user:
        print("❌ Test user already exists!")
        print(f"Email: test@example.com")
        print(f"Username: {existing_user.username}")
        return existing_user
    
    # Create test user
    test_user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        date_of_birth=date(1990, 1, 1),
        role=UserRole.USER,
        kyc_status=KYCStatus.VERIFIED,
        is_active=True,
        is_banned=False
    )
    
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    
    # Create wallet for test user
    wallet = Wallet(
        user_id=test_user.id,
        balance=1000.0  # Give test user some credits
    )
    db.add(wallet)
    db.commit()
    
    print("✅ Test user created successfully!")
    print("")
    print("=" * 50)
    print("TEST USER CREDENTIALS")
    print("=" * 50)
    print(f"Email:    test@example.com")
    print(f"Password: testpassword")
    print(f"Username: testuser")
    print("=" * 50)
    
    db.close()
    return test_user

if __name__ == "__main__":
    create_test_user()