# Quick Fix for 401 Unauthorized Issue

## The Problem
All API calls are returning **401 Unauthorized** even after login.

## Root Cause
The JWT tokens are being generated but something is wrong with validation. This could be:
1. Backend restarted with a different JWT_SECRET_KEY
2. Token format mismatch
3. Database connection issue during token validation

## Quick Fix Steps

### Option 1: Restart Backend (Most Likely Fix)

The backend might have restarted and generated new tokens with a different secret. This invalidates all old tokens.

```bash
# Stop the backend (Ctrl+C in the terminal running it)
# Then restart:
cd Gidanbanta/backend
.\venv\Scripts\activate
python main.py
```

Then in your browser:
1. **Clear localStorage**: F12 → Application → Local Storage → Right-click → Clear
2. **Refresh the page**
3. **Login again**

### Option 2: Use the Debug Tool

I created a test page to help debug:

1. Open `Gidanbanta/test_login_flow.html` in your browser
2. Click "Test Login" - this will login and store the token
3. Click "Check Storage" - verify token is stored
4. Click "Test /v1/users/me" - test if token works
5. Click "Test /v1/matches/calendar/matches" - test matches endpoint

This will show you exactly where the problem is.

### Option 3: Manual Test

Open browser console (F12 → Console) and run:

```javascript
// Clear old tokens
localStorage.clear();

// Login
fetch('http://localhost:4000/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'debug@test.com',
    password: 'Debug123!'
  })
})
.then(r => r.json())
.then(data => {
  console.log('Login response:', data);
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  console.log('✅ Tokens stored');
  
  // Test the token
  return fetch('http://localhost:4000/v1/users/me', {
    headers: { 'Authorization': `Bearer ${data.access_token}` }
  });
})
.then(r => r.json())
.then(data => {
  console.log('User data:', data);
});
```

## What to Check

### In Browser DevTools (F12):

1. **Console Tab**: Look for JavaScript errors
2. **Network Tab**: 
   - Click on a failed request (401)
   - Check "Request Headers" - is `Authorization: Bearer ...` present?
   - Check "Response" - what error message?
3. **Application Tab**:
   - Local Storage → http://localhost:3000
   - Are `access_token` and `refresh_token` present?

## Most Likely Solution

**Just restart the backend and clear browser localStorage:**

```bash
# Terminal 1: Restart backend
cd Gidanbanta/backend
python main.py

# Browser: Clear storage
# F12 → Application → Local Storage → Right-click → Clear
# Then refresh and login again
```

## If Still Not Working

Check these in browser console after login:

```javascript
// Check if token exists
console.log('Token:', localStorage.getItem('access_token'));

// Test API call manually
fetch('http://localhost:4000/v1/users/me', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
})
.then(r => r.json())
.then(data => console.log('API Response:', data));
```

Share the console output with me!
