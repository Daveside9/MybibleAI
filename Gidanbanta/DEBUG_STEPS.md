# Debug Steps - 401 Unauthorized Issue

## Current Problem
All API calls are returning **401 Unauthorized**, which means the authentication token is not working.

## Step 1: Check if Token is Stored

1. Open browser DevTools (F12)
2. Go to **Application** tab
3. Expand **Local Storage** → `http://localhost:3000`
4. Look for these keys:
   - `access_token`
   - `refresh_token`

**If you DON'T see these keys:**
- The login is not storing the token properly
- This is the root cause

**If you DO see these keys:**
- Copy the `access_token` value
- We need to test if it's valid

## Step 2: Test the Token Manually

If you have a token in localStorage, let's test it:

1. Copy the `access_token` value from localStorage
2. Open a new terminal
3. Run this command (replace YOUR_TOKEN with the actual token):

```bash
curl -X GET "http://localhost:4000/v1/users/me" -H "Authorization: Bearer YOUR_TOKEN"
```

**If this returns user data:** The token is valid, but the frontend isn't sending it correctly
**If this returns 401:** The token is invalid or expired

## Step 3: Check Network Request Headers

1. In DevTools, go to **Network** tab
2. Refresh the page
3. Click on any failed request (red, 401 status)
4. Look at **Request Headers**
5. Check if you see: `Authorization: Bearer eyJ...`

**If Authorization header is MISSING:**
- The frontend is not sending the token
- This is the issue

**If Authorization header is PRESENT:**
- The token is being sent but is invalid
- Backend might have restarted with a different secret key

## Most Likely Fix

The issue is that the token is not being stored or sent. Let me check the login flow...
