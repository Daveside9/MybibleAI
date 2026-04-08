from jose import jwt, JWTError
import json
from app.core.config import settings

# The token from the browser
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsImV4cCI6MTc2NDg1OTE5OCwidHlwZSI6ImFjY2VzcyJ9.4Vh4PxMYj2dybVnA5Timz54bqzI35nhhR6DtTQxzybw"

print("=" * 80)
print("TOKEN VALIDATION TEST")
print("=" * 80)
print()

# Decode without verification
print("1. Decoding token payload (without verification)...")
try:
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM], options={"verify_signature": False})
    print("✅ Payload decoded:")
    print(json.dumps(payload, indent=2))
    print()
except Exception as e:
    print(f"❌ Error: {e}")
    print()

# Try to verify with current secret
print("2. Verifying token with current JWT_SECRET_KEY...")
print(f"   JWT_SECRET_KEY: {settings.JWT_SECRET_KEY}")
print(f"   JWT_ALGORITHM: {settings.JWT_ALGORITHM}")
print()

try:
    verified = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    print("✅ TOKEN IS VALID!")
    print("User ID:", verified.get('sub'))
    print("Expires:", verified.get('exp'))
    print()
    print("This means the backend SHOULD accept this token.")
    print("If it's still returning 401, there might be a database issue.")
except jwt.ExpiredSignatureError:
    print("❌ TOKEN HAS EXPIRED")
    print("The token is valid but has passed its expiration time.")
    print("Solution: Login again to get a fresh token.")
except jwt.JWTError as e:
    print("❌ TOKEN SIGNATURE IS INVALID")
    print(f"Error: {e}")
    print()
    print("This means the token was signed with a DIFFERENT JWT_SECRET_KEY.")
    print("Solution:")
    print("1. Make sure the backend is using the JWT_SECRET_KEY from .env")
    print("2. Restart the backend")
    print("3. Clear browser localStorage and login again")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print()
print("=" * 80)
