// Copy and paste this into your browser console (F12 → Console)
// This will test a fresh login and immediately use the token

console.log('🧪 Testing Fresh Login Flow...\n');

// Step 1: Clear old tokens
localStorage.removeItem('access_token');
localStorage.removeItem('refresh_token');
console.log('✅ Cleared old tokens\n');

// Step 2: Login
console.log('🔐 Logging in...');
fetch('http://localhost:4000/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'debug@test.com',  // Change this to your email
    password: 'Debug123!'      // Change this to your password
  })
})
.then(response => {
  console.log(`Login response status: ${response.status}`);
  return response.json();
})
.then(data => {
  if (data.access_token) {
    console.log('✅ Login successful!');
    console.log('Token:', data.access_token.substring(0, 50) + '...');
    console.log('User:', data.user);
    
    // Store tokens
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    console.log('✅ Tokens stored in localStorage\n');
    
    // Step 3: Immediately test the token
    console.log('🧪 Testing token with /v1/users/me...');
    return fetch('http://localhost:4000/v1/users/me', {
      headers: {
        'Authorization': `Bearer ${data.access_token}`,
        'Content-Type': 'application/json'
      }
    });
  } else {
    throw new Error('No access_token in response: ' + JSON.stringify(data));
  }
})
.then(response => {
  console.log(`/v1/users/me response status: ${response.status}`);
  return response.json();
})
.then(data => {
  if (data.id) {
    console.log('✅ Token works! User data:', data);
    console.log('\n🎉 SUCCESS! Now refresh the page.');
  } else {
    console.log('❌ Token validation failed:', data);
  }
})
.catch(error => {
  console.error('❌ Error:', error);
});
