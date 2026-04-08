"""
Create Admin User Script
Run this to create the first admin account
"""
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole, KYCStatus
from app.models.wallet import Wallet
from datetime import date

def create_admin():
    db = SessionLocal()
    
    # Check if admin already exists
    existing_admin = db.query(User).filter(User.email == "admin@matchhang.com").first()
    if existing_admin:
        print("❌ Admin user already exists!")
        print(f"Email: admin@matchhang.com")
        return
    
    # Create admin user
    admin = User(
        email="admin@matchhang.com",
        username="admin",
        hashed_password=get_password_hash("Admin@123"),  # Change this password!
        full_name="Admin User",
        date_of_birth=date(1990, 1, 1),
        role=UserRole.ADMIN,
        kyc_status=KYCStatus.VERIFIED,
        is_active=True,
        is_banned=False
    )
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    # Create wallet for admin
    wallet = Wallet(
        user_id=admin.id,
        balance=1000000.0  # Give admin 1M credits for testing
    )
    db.add(wallet)
    db.commit()
    
    print("✅ Admin user created successfully!")
    print("")
    print("=" * 50)
    print("ADMIN CREDENTIALS")
    print("=" * 50)
    print(f"Email:    admin@matchhang.com")
    print(f"Password: Admin@123")
    print("=" * 50)
    print("")
    print("⚠️  IMPORTANT: Change this password after first login!")
    print("")
    print("You can now:")
    print("1. Login at: http://localhost:3000/login")
    print("2. Access admin dashboard at: http://localhost:3000/admin")
    print("3. Use API at: http://localhost:4000/docs")
    
    db.close()

if __name__ == "__main__":
    create_admin()
