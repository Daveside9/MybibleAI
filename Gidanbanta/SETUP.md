# MatchHang Setup Guide

## Quick Start

### 1. Backend Setup

```bash
cd Gidanbanta/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your database credentials

# Create database (PostgreSQL)
# CREATE DATABASE matchhang;

# Run server
python main.py
```

Backend will run on: http://localhost:4000

### 2. Frontend Setup

```bash
cd Gidanbanta/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run on: http://localhost:3000

## What's Built

### ✅ Backend (FastAPI)
- User authentication (signup/login with JWT)
- Age gating (18+ for purchases, 13+ minimum)
- Wallet system (virtual credits)
- Match management
- Real-time chat (Socket.IO)
- Database models (User, Wallet, Transaction, Match, ChatMessage)

### ✅ Frontend (Next.js)
- Landing page
- Signup page (with age validation)
- Login page
- Dashboard (shows matches, wallet balance)
- Auth context (global state management)
- API client (handles all backend requests)

## Features

### Authentication
- **Signup**: Email, username, password, DOB
- **Age Gating**: 
  - Under 13: Cannot sign up
  - 13-17: Spectator mode (watch only, 3 free messages)
  - 18+: Full access (can purchase)
- **KYC**: Required for purchases and withdrawals

### Dashboard
- View today's featured matches
- Wallet balance display
- Quick actions (Predictions, Fantasy, Wallet)
- User profile with role display

### Wallet
- Virtual credits (1₦ = 1 credit)
- Top-up via Opay/PalmPay/Moniepoint (coming soon)
- Transaction history
- Separate tracking: deposited vs winnings

## Next Steps

1. **Test the auth flow**:
   - Sign up with different ages
   - Login
   - View dashboard

2. **Add match room** (coming next):
   - Video streaming
   - Real-time chat
   - Camera reactions
   - Per-match chat unlock (₦100)

3. **Payment integration**:
   - Opay SDK
   - PalmPay SDK
   - Moniepoint SDK

4. **Fantasy football**:
   - Team builder
   - Contests
   - Leaderboards

## Database Schema

### Users
- id, email, username, password (hashed)
- date_of_birth, role, kyc_status
- is_active, is_banned

### Wallet
- user_id, balance
- deposited_amount, winnings_amount

### Transactions
- user_id, type, amount, status
- provider, match_id

### Matches
- title, home_team, away_team
- scores, status, stream_url
- scheduled_at, is_featured

### ChatMessages
- match_id, user_id, content
- type (text/reaction/emoji)
- moderation_status

## API Endpoints

### Auth
- `POST /v1/auth/signup` - Register
- `POST /v1/auth/login` - Login

### Users
- `GET /v1/users/me` - Current user

### Wallet
- `GET /v1/wallet` - Balance
- `GET /v1/wallet/transactions` - History

### Matches
- `GET /v1/matches/today` - Featured matches
- `GET /v1/matches/{id}` - Match details

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@localhost:5432/matchhang
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:4000
NEXT_PUBLIC_SOCKET_URL=http://localhost:4000
```

## Troubleshooting

### Backend won't start
- Check PostgreSQL is running
- Check Redis is running
- Verify .env file exists
- Check database credentials

### Frontend can't connect
- Verify backend is running on port 4000
- Check NEXT_PUBLIC_API_URL in .env.local
- Check CORS settings in backend

### Auth not working
- Clear localStorage
- Check JWT_SECRET_KEY matches in backend
- Verify tokens are being saved

## Production Checklist

- [ ] Set DEBUG=False
- [ ] Use production database
- [ ] Set strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Enable HTTPS
- [ ] Setup proper CORS
- [ ] Configure payment providers
- [ ] Setup moderation tools
- [ ] Enable rate limiting
- [ ] Setup monitoring
- [ ] Backup database regularly

## Support

For issues, check:
1. Backend logs (console output)
2. Frontend console (browser DevTools)
3. Network tab (API requests)
4. Database connection

## License

Proprietary - MatchHang 2025
