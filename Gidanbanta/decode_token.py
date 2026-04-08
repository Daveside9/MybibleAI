import jwt
import json

# The token from the browser
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsImV4cCI6MTc2NDg1OTE5OCwidHlwZSI6ImFjY2VzcyJ9.4Vh4PxMYj2dybVnA5Timz54bqzI35nhhR6DtTQxzybw"

# Decode without verification to see the payload
try:
    # Decode header
    header = jwt.get_unverified_header(token)
    print("Token Header:")
    print(json.dumps(header, indent=2))
    print()
    
    # Decode payload (without verifying signature)
    payload = jwt.decode(token, options={"verify_signature": False})
    print("Token Payload:")
    print(json.dumps(payload, indent=2))
    print()
    
    # Try to verify with the secret from .env
    from app.core.config import settings
    print(f"JWT_SECRET_KEY from .env: {settings.JWT_SECRET_KEY}")
    print()
    
    try:
        verified = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        print("✅ Token is VALID with current JWT_SECRET_KEY")
        print(json.dumps(verified, indent=2))
    except jwt.InvalidSignatureError:
        print("❌ Token signature is INVALID")
        print("This means the token was signed with a DIFFERENT JWT_SECRET_KEY")
        print()
        print("SOLUTION: The backend must have restarted or the JWT_SECRET_KEY changed.")
        print("You need to login again to get a new token signed with the current key.")
    except jwt.ExpiredSignatureError:
        print("❌ Token has EXPIRED")
        print("You need to login again to get a fresh token.")
    except Exception as e:
        print(f"❌ Token validation error: {e}")
        
except Exception as e:
    print(f"Error decoding token: {e}")
