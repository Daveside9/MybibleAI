"""
Test the exact API call the frontend makes
"""
import requests
import json

print("Testing MatchHang API Endpoints")
print("=" * 80)

# Step 1: Create/Login a test user
print("\n1. Creating test user...")
signup_data = {
    "email": "debug@test.com",
    "username": "debuguser",
    "password": "Debug123!",
    "date_of_birth": "1990-01-01"
}

response = requests.post(
    "http://localhost:4000/v1/auth/signup",
    json=signup_data
)

if response.status_code in [200, 201]:
    data = response.json()
    token = data.get('access_token')
    print(f"✅ User created successfully")
    print(f"   Token: {token[:50]}...")
elif response.status_code == 400:
    # User might already exist, try login
    print("⚠️  User exists, trying login...")
    response = requests.post(
        "http://localhost:4000/v1/auth/login",
        json={"email": signup_data["email"], "password": signup_data["password"]}
    )
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        print(f"✅ Logged in successfully")
        print(f"   Token: {token[:50]}...")
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        exit(1)
else:
    print(f"❌ Signup failed: {response.status_code}")
    print(response.text)
    exit(1)

# Step 2: Test /v1/users/me
print("\n2. Testing /v1/users/me...")
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:4000/v1/users/me", headers=headers)

if response.status_code == 200:
    user = response.json()
    print(f"✅ User endpoint works")
    print(f"   Username: {user.get('username')}")
    print(f"   Email: {user.get('email')}")
else:
    print(f"❌ User endpoint failed: {response.status_code}")
    print(response.text)

# Step 3: Test /v1/wallet
print("\n3. Testing /v1/wallet...")
response = requests.get("http://localhost:4000/v1/wallet", headers=headers)

if response.status_code == 200:
    wallet = response.json()
    print(f"✅ Wallet endpoint works")
    print(f"   Balance: ₦{wallet.get('balance', 0)}")
else:
    print(f"❌ Wallet endpoint failed: {response.status_code}")
    print(response.text)

# Step 4: Test /v1/matches/calendar/matches (THE IMPORTANT ONE)
print("\n4. Testing /v1/matches/calendar/matches...")
params = {
    "start_date": "2025-12-04",
    "end_date": "2025-12-04"
}
response = requests.get(
    "http://localhost:4000/v1/matches/calendar/matches",
    headers=headers,
    params=params
)

print(f"   URL: {response.url}")
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    matches = data.get('matches', [])
    print(f"✅ Calendar endpoint works")
    print(f"   Total matches: {data.get('total', 0)}")
    print(f"   Cached: {data.get('cached', False)}")
    print(f"\n   Matches for 2025-12-04:")
    if matches:
        for match in matches:
            print(f"   - {match['home_team']} vs {match['away_team']}")
            print(f"     Time: {match['scheduled_time']}")
            print(f"     Status: {match['status']}")
            print(f"     Odds: H:{match['home_odds']} D:{match['draw_odds']} A:{match['away_odds']}")
            print()
    else:
        print("   ⚠️  No matches returned (but API works)")
else:
    print(f"❌ Calendar endpoint failed: {response.status_code}")
    print(response.text)

# Step 5: Test /v1/matches/calendar/leagues
print("\n5. Testing /v1/matches/calendar/leagues...")
response = requests.get(
    "http://localhost:4000/v1/matches/calendar/leagues",
    headers=headers,
    params=params
)

if response.status_code == 200:
    leagues = response.json()
    print(f"✅ Leagues endpoint works")
    print(f"   Total leagues: {len(leagues)}")
    for league in leagues:
        print(f"   - {league['name']} ({league['country']}): {league['match_count']} matches")
else:
    print(f"❌ Leagues endpoint failed: {response.status_code}")
    print(response.text)

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("\nIf all tests passed ✅, the backend is working correctly.")
print("The issue is likely in the frontend:")
print("1. Check browser console for JavaScript errors")
print("2. Check Network tab to see if requests are being made")
print("3. Check if token is being stored in localStorage")
print("\nTo debug frontend:")
print("1. Open http://localhost:3000")
print("2. Press F12 (DevTools)")
print("3. Go to Console tab")
print("4. Login and watch for errors")
print("5. Go to Network tab")
print("6. Refresh and check if API calls are made")
