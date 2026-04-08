"""
Verify User KYC Script
Run this to verify KYC for a specific user (for testing purposes)
"""
from app.core.database import SessionLocal
from app.models.user import User, KYCStatus
import sys

def verify_user_kyc(email: str):
    db = SessionLocal()
    
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        print(f"❌ User with email '{email}' not found!")
        db.close()
        return
    
    # Check if user is already verified
    if user.kyc_status == KYCStatus.VERIFIED:
        print(f"✅ User '{user.username}' is already KYC verified!")
        db.close()
        return
    
    # Verify KYC
    user.kyc_status = KYCStatus.VERIFIED
    db.commit()
    
    print("✅ KYC verification successful!")
    print("")
    print("=" * 50)
    print("USER DETAILS")
    print("=" * 50)
    print(f"Email:       {user.email}")
    print(f"Username:    {user.username}")
    print(f"Age:         {user.age}")
    print(f"KYC Status:  {user.kyc_status.value}")
    print(f"Can Purchase: {user.can_purchase}")
    print("=" * 50)
    
    db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_user_kyc.py <email>")
        print("Example: python verify_user_kyc.py user@example.com")
        sys.exit(1)
    
    email = sys.argv[1]
    verify_user_kyc(email)
