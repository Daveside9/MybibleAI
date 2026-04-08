"""
Comprehensive System Test Script
Tests backend, database, and API endpoints
"""
import requests
import sqlite3
from datetime import datetime, timedelta
import json

print("=" * 100)
print("MATCHHANG SYSTEM TEST")
print("=" * 100)

# 1. Check Database
print("\n1. DATABASE CHECK")
print("-" * 100)
try:
    conn = sqlite3.connect('backend/matchhang.db')
    cursor = conn.cursor()
    
    # Count matches
    cursor.execute('SELECT COUNT(*) FROM matches')
    match_count = cursor.fetchone()[0]
    print(f"✅ Total matches in database: {match_count}")
    
    # Check today's matches
    today = datetime.now().date()
    cursor.execute('''
        SELECT home_team, away_team, scheduled_at, status 
        FROM matches 
        WHERE DATE(scheduled_at) = ? 
        ORDER BY scheduled_at
    ''', (str(today),))
    today_matches = cursor.fetchall()
    
    print(f"✅ Matches for today ({today}): {len(today_matches)}")
    for m in today_matches:
        print(f"   - {m[0]} vs {m[1]} at {m[2]} ({m[3]})")
    
    # Check users
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]
    print(f"✅ Total users: {user_count}")
    
    conn.close()
except Exception as e:
    print(f"❌ Database error: {e}")

# 2. Check Backend Server
print("\n2. BACKEND SERVER CHECK")
print("-" * 100)
backend_url = "http://localhost:4000"

try:
    response = requests.get(f"{backend_url}/health", timeout=5)
    if response.status_code == 200:
        print(f"✅ Backend server is running at {backend_url}")
    else:
        print(f"⚠️  Backend responded with status {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"❌ Backend server is NOT running at {backend_url}")
    print("   Run: cd backend && python main.py")
except Exception as e:
    print(f"❌ Backend check error: {e}")

# 3. Test API Endpoints (without auth)
print("\n3. API ENDPOINTS CHECK")
print("-" * 100)

# Test login endpoint
print("Testing login endpoint...")
try:
    response = requests.post(
        f"{backend_url}/v1/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"},
        timeout=5
    )
    if response.status_code in [200, 401, 422]:
        print(f"✅ Login endpoint is accessible (status: {response.status_code})")
    else:
        print(f"⚠️  Login endpoint returned unexpected status: {response.status_code}")
except Exception as e:
    print(f"❌ Login endpoint error: {e}")

# 4. Test with actual login (if you have test credentials)
print("\n4. AUTHENTICATED API TEST")
print("-" * 100)
print("To test authenticated endpoints, you need to:")
print("1. Create a test user via signup")
print("2. Login to get an access token")
print("3. Use the token to access protected endpoints")
print("\nExample:")
print("  POST /v1/auth/signup")
print("  POST /v1/auth/login")
print("  GET /v1/matches/calendar/matches?start_date=2025-12-04&end_date=2025-12-04")

# 5. Check Frontend
print("\n5. FRONTEND CHECK")
print("-" * 100)
frontend_url = "http://localhost:3000"
try:
    response = requests.get(frontend_url, timeout=5)
    if response.status_code == 200:
        print(f"✅ Frontend is running at {frontend_url}")
    else:
        print(f"⚠️  Frontend responded with status {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"❌ Frontend is NOT running at {frontend_url}")
    print("   Run: cd frontend && npm run dev")
except Exception as e:
    print(f"❌ Frontend check error: {e}")

# 6. Summary
print("\n" + "=" * 100)
print("SUMMARY")
print("=" * 100)
print("\nIf you see issues:")
print("1. ❌ Backend not running → cd backend && python main.py")
print("2. ❌ Frontend not running → cd frontend && npm run dev")
print("3. ❌ No matches → cd backend && python create_test_matches.py")
print("4. ❌ Login redirects → Check browser console for errors")
print("5. ❌ No matches display → Check browser Network tab for API calls")
print("\nFor login/refresh issues:")
print("- Open browser DevTools (F12)")
print("- Go to Application → Local Storage")
print("- Check if 'access_token' exists after login")
print("- Check Console tab for errors")
print("- Check Network tab for failed API calls")
print("=" * 100)
