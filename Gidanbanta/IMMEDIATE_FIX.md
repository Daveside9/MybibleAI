# IMMEDIATE FIX - Do This Now

## The Problem
You have an **old invalid token** stored in localStorage that's causing 401 errors.

## The Fix (Takes 30 seconds)

### Step 1: Clear the Old Token
In your browser console (F12 → Console), paste this and press Enter:

```javascript
localStorage.clear();
console.log('✅ Cleared! Now refresh the page.');
```

### Step 2: Refresh the Page
Press `Ctrl + R` or click the refresh button

### Step 3: Login Again
- You'll be redirected to the login page
- Login with your credentials
- You should now see the dashboard with matches

## That's It!

The old token was generated with a different JWT secret key (probably from when the backend restarted). Clearing it and logging in again will generate a fresh valid token.

---

## If You Still See 401 Errors After This

Then we have a different problem. Run this in the console after logging in:

```javascript
// Test if the new token works
const token = localStorage.getItem('access_token');
console.log('Token:', token ? token.substring(0, 30) + '...' : 'NOT FOUND');

fetch('http://localhost:4000/v1/users/me', {
  headers: { 'Authorization': `Bearer ${token}` }
})
.then(r => r.json())
.then(data => console.log('Result:', data));
```

And share the output with me.
