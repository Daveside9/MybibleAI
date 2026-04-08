# Admin Dashboard Guide

## Default Admin Credentials

**Email:** `admin@matchhang.com`  
**Password:** `Admin@123`

⚠️ **IMPORTANT:** Change this password after first login!

---

## Setup Admin Account

### Step 1: Create Admin User

Run this command in the backend directory:

```bash
cd backend
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

python create_admin.py
```

This will create the admin account with:
- Email: admin@matchhang.com
- Password: Admin@123
- Role: Admin
- 1,000,000 credits (for testing)

### Step 2: Login

1. Go to: http://localhost:3000/login
2. Enter admin credentials
3. You'll be redirected to the dashboard

### Step 3: Access Admin Dashboard

Visit: http://localhost:3000/admin

---

## Admin Dashboard Features

### 📊 Statistics Overview
- **Total Users:** All registered users
- **Active Users:** Currently active users
- **Total Matches:** All matches created
- **Live Matches:** Currently live matches

### ⚽ Match Management

**Create Match:**
1. Click "+ Create Match" button
2. Fill in:
   - Match Title (e.g., "Premier League - Chelsea vs Arsenal")
   - Home Team
   - Away Team
   - Scheduled Time
3. Click "Create Match"

**Start Match Live:**
- Click "Start Live" button on scheduled match
- Match status changes to "live"
- Users can now join and chat

**End Match:**
- Click "End Match" button on live match
- Match status changes to "finished"
- Chat access expires

---

## Admin API Endpoints

All admin endpoints require authentication with admin role.

### Get Platform Stats
```
GET /v1/admin/stats
Authorization: Bearer {token}
```

Response:
```json
{
  "users": {
    "total": 100,
    "active": 95,
    "banned": 5
  },
  "matches": {
    "total": 50,
    "live": 2
  },
  "wallet": {
    "total_balance": 500000.0
  }
}
```

### Create Match
```
POST /v1/admin/matches
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Premier League - Chelsea vs Arsenal",
  "home_team": "Chelsea",
  "away_team": "Arsenal",
  "scheduled_at": "2025-12-10T15:00:00",
  "is_featured": true
}
```

### Update Match Status
```
PUT /v1/admin/matches/{match_id}/status?status=live
Authorization: Bearer {token}
```

Status options: `scheduled`, `live`, `finished`, `cancelled`

### Update Match Score
```
PUT /v1/admin/matches/{match_id}/score?home_score=2&away_score=1
Authorization: Bearer {token}
```

### List All Matches
```
GET /v1/admin/matches?skip=0&limit=50
Authorization: Bearer {token}
```

### Ban User
```
POST /v1/admin/users/{user_id}/ban
Authorization: Bearer {token}
Content-Type: application/json

{
  "reason": "Inappropriate behavior"
}
```

### Unban User
```
POST /v1/admin/users/{user_id}/unban
Authorization: Bearer {token}
```

---

## Testing the Admin Dashboard

### 1. Create Admin Account
```bash
cd backend
python create_admin.py
```

### 2. Start Backend
```bash
python main.py
```

### 3. Start Frontend
```bash
cd ../frontend
npm run dev
```

### 4. Login as Admin
- Go to: http://localhost:3000/login
- Email: admin@matchhang.com
- Password: Admin@123

### 5. Access Admin Dashboard
- Go to: http://localhost:3000/admin
- You should see stats and match management

### 6. Create a Test Match
1. Click "+ Create Match"
2. Fill in:
   - Title: "Test Match - Team A vs Team B"
   - Home Team: "Team A"
   - Away Team: "Team B"
   - Scheduled Time: (select a future time)
3. Click "Create Match"

### 7. Start Match Live
1. Find your match in the list
2. Click "Start Live"
3. Match is now live!

### 8. Test as Regular User
1. Open incognito window
2. Go to: http://localhost:3000/signup
3. Create a regular user account
4. Go to dashboard
5. You should see the live match
6. Click "Join Room" to test chat

---

## Admin Permissions

### Admin Role Can:
- ✅ View platform statistics
- ✅ Create matches
- ✅ Update match status (scheduled → live → finished)
- ✅ Update match scores
- ✅ Ban/unban users
- ✅ View all matches
- ✅ Access admin dashboard

### Moderator Role Can:
- ✅ View platform statistics
- ✅ Update match status
- ✅ Ban/unban users
- ✅ Access admin dashboard
- ❌ Create matches (admin only)

### Regular User Cannot:
- ❌ Access admin dashboard
- ❌ Create matches
- ❌ Ban users
- ❌ View platform stats

---

## Security Notes

### Change Default Password
After first login, update the admin password:

1. Login as admin
2. Go to profile settings
3. Change password to something secure

### Create Additional Admins
To create more admin accounts, modify `create_admin.py`:

```python
admin = User(
    email="newadmin@matchhang.com",  # Change email
    username="newadmin",              # Change username
    hashed_password=get_password_hash("SecurePassword123!"),
    # ... rest of the code
)
```

Then run: `python create_admin.py`

### Production Security
For production:
- Use strong passwords
- Enable 2FA (to be implemented)
- Limit admin access
- Monitor admin actions
- Use audit logs

---

## Troubleshooting

### "Admin user already exists"
The admin account is already created. Use the existing credentials or delete the user from the database first.

### "403 Forbidden" on admin endpoints
Your user doesn't have admin role. Check:
1. You're logged in as admin
2. Token is valid
3. User role is "admin" or "moderator"

### Admin dashboard shows "Access Denied"
Your account doesn't have admin privileges. Login with admin credentials.

### Can't create matches
Check:
1. All fields are filled
2. Scheduled time is in correct format
3. You're logged in as admin
4. Backend is running

---

## API Documentation

For complete API documentation, visit:
http://localhost:4000/docs

This shows all endpoints with:
- Request/response schemas
- Try-it-out functionality
- Authentication requirements

---

## Next Steps

1. ✅ Create admin account
2. ✅ Login to admin dashboard
3. ✅ Create test matches
4. ✅ Test match lifecycle (scheduled → live → finished)
5. ✅ Test user chat access
6. [ ] Add more admin features (user management, analytics)
7. [ ] Implement moderation tools
8. [ ] Add audit logging

---

**Admin Dashboard Ready!** 🎉

For questions or issues, check the logs:
- Backend: Terminal where `python main.py` is running
- Frontend: Browser console (F12)
