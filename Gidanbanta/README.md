# MatchHang (Gidanbanta)

Live match streaming + social viewing rooms with virtual credits, camera reactions, and fantasy football.

## Project Structure

```
Gidanbanta/
├── frontend/          # Next.js 14 (React + TypeScript)
├── backend/           # NestJS (Node.js + TypeScript) - Coming soon
└── README.md
```

## Tech Stack

### Frontend
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Socket.IO Client (real-time chat)
- HLS.js (video streaming)

### Backend
- FastAPI (Python 3.11+)
- PostgreSQL (users, transactions, fantasy)
- Redis (chat, presence, rate limiting)
- Socket.IO (real-time)
- SQLAlchemy ORM
- Celery (background tasks)
- Payment integrations (Opay, PalmPay, Moniepoint)

## Features

### MVP
- ✅ Landing page
- ✅ Auth (signup/login with age gating)
- ✅ Dashboard with live match
- ✅ Match room (stream + chat)
- ✅ Wallet (virtual credits)
- ✅ Basic moderation

### v1
- Camera reactions
- KYC verification
- Payment provider integrations
- Fantasy football
- Paid contests

## Getting Started

### Quick Start (Development)

**1. Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env  # Edit with your credentials
python main.py
```

**2. Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Visit:
- Frontend: http://localhost:3000
- API Docs: http://localhost:4000/docs
- API Health: http://localhost:4000/health

## Environment Variables

Create `.env.local` in frontend:
```
NEXT_PUBLIC_API_URL=http://localhost:4000
NEXT_PUBLIC_SOCKET_URL=http://localhost:4000
```

## Design System

- Primary: Navy #071226
- Accent: Blue #0B6CF1
- Highlight: Cyan #00C2FF
- Success: #32D583
- Danger: #FF5964

## Monetization

- Virtual credits (1₦ = 1 credit)
- Per-match chat access: 100₦
- 3 free messages per match
- Fantasy contests (paid entry)

## Compliance

- Age gating (18+)
- KYC required for purchases
- Content moderation
- No real-money gambling

## License

Proprietary
