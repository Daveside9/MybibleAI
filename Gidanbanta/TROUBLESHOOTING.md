# Troubleshooting Guide

## Issue: No Matches Displaying & Login Redirect on Refresh

### Quick Diagnosis

Both your **backend** and **frontend** are running correctly. The issues are:

1. **Authentication tokens not persisting** on page refresh
2. **Matches not loading** even though they exist in the database

---

## Solution Steps

### Step 1: Check Browser Console

1. Open your browser at `http://localhost:3000`
2. Press `F12` to open DevTools
3. Go to the **Console** tab
4. Look for any red error messages
5. Take a screenshot and share if you see errors

### Step 2: Check Local Storage

1. In DevTools, go to **Application** tab
2. Expand **Local Storage** → `http://localhost:3000`
3. After logging in, check if you see:
   - `access_token`
   - `refresh_token`
4. If these disappear after refresh, that's the problem

### Step 3: Check Network Requests

1. In DevTools, go to **Network** tab
2. Refresh the dashboard page
3. Look for these API calls:
   - `GET /v1/users/me` (should return 200)
   - `GET /v1/matches/calendar/matches?start_date=...` (should return 200)
4. Click on any failed requests (red) to see the error

### Step 4: Test API Directly

Open a new terminal and run these commands to test the API:

```bash
# Test 1: Check if matches exist for today
cd backend
python check_matches.py
```

You should see matches for December 4-10, 2025.

```bash
# Test 2: Create a test user and login
curl -X POST http://localhost:4000/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@test.com",
    "username": "testuser",
    "password": "Test123!",
    "date_of_birth": "1990-01-01"
  }'
```

This will return an `access_token`. Copy it.

```bash
# Test 3: Get matches with the token
curl -X GET "http://localhost:4000/v1/matches/calendar/matches?start_date=2025-12-04&end_date=2025-12-04" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Replace `YOUR_TOKEN_HERE` with the token from step 2.

---

## Common Issues & Fixes

### Issue A: "401 Unauthorized" on API calls

**Cause**: Token is invalid or expired

**Fix**:
1. Clear browser Local Storage
2. Log out and log in again
3. Check if token is being sent in requests (Network tab → Headers)

### Issue B: Matches array is empty `[]`

**Cause**: No matches in database for selected date

**Fix**:
```bash
cd backend
python create_test_matches.py
```

### Issue C: Page redirects to login on refresh

**Cause**: Auth context loses user state

**Fix**: I've already updated `AuthContext.tsx` to handle this better. Make sure your frontend is using the latest code.

### Issue D: CORS errors in console

**Cause**: Backend not allowing frontend origin

**Fix**: Check `backend/.env` has:
```
CORS_ORIGINS=["http://localhost:3000"]
```

---

## Database Status

Your database currently has:
- **11 matches** scheduled for Dec 4-10, 2025
- Matches for today (Dec 4):
  - Juventus vs AC Milan (LIVE)
  - Chelsea vs Arsenal (SCHEDULED)
  - Manchester United vs Liverpool (SCHEDULED)

---

## What I Fixed

1. **AuthContext.tsx**: Improved error handling so tokens aren't cleared on network errors
2. **Added debugging scripts**: 
   - `check_matches.py` - View all matches in database
   - `test_system.py` - Comprehensive system check

---

## Next Steps

1. **Open browser DevTools** (F12)
2. **Login to your account**
3. **Check Console tab** for errors
4. **Check Network tab** for failed API calls
5. **Share screenshots** of any errors you see

The most likely issue is that the API calls are failing silently. The Network tab will show us exactly what's happening.

---

## Quick Test Commands

```bash
# Check if backend is running
curl http://localhost:4000/health

# Check if frontend is running
curl http://localhost:3000

# View matches in database
cd backend && python check_matches.py

# Create test matches
cd backend && python create_test_matches.py
```

---

## Still Having Issues?

Share screenshots of:
1. Browser Console (F12 → Console tab)
2. Network tab showing failed requests
3. Local Storage (F12 → Application → Local Storage)

This will help me identify the exact problem!
