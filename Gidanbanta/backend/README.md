# MatchHang Backend (FastAPI)

Real-time match streaming API with Socket.IO, PostgreSQL, and Redis.

## Tech Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Primary database
- **Redis** - Caching, sessions, real-time data
- **Socket.IO** - Real-time chat
- **SQLAlchemy** - ORM
- **Celery** - Background tasks for match synchronization

## Setup

### 1. Install Python 3.11+

Make sure you have Python 3.11 or higher installed.

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL

Install PostgreSQL and create a database:

```sql
CREATE DATABASE matchhang;
CREATE USER matchhang_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE matchhang TO matchhang_user;
```

### 5. Setup Redis

Install Redis:
- **Windows**: Download from https://github.com/microsoftarchive/redis/releases
- **Mac**: `brew install redis`
- **Linux**: `sudo apt-get install redis-server`

Start Redis:
```bash
redis-server
```

### 6. Environment Variables

Copy `.env.example` to `.env` and update:

```bash
cp .env.example .env
```

Update these values:
```
DATABASE_URL=postgresql://matchhang_user:your_password@localhost:5432/matchhang
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
```

### 7. Create Database Tables

```bash
# Using Alembic (recommended)
alembic upgrade head

# Or create tables directly (for development)
python -c "from app.core.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"
```

### 8. Run the Server

```bash
# Development
python main.py

# Or with uvicorn
uvicorn main:socket_app --reload --host 0.0.0.0 --port 4000
```

Visit:
- API: http://localhost:4000
- Docs: http://localhost:4000/docs
- Health: http://localhost:4000/health

### 9. Run Celery Worker (Optional - for match synchronization)

In a separate terminal, start the Celery worker with beat scheduler:

```bash
# Windows
start_celery.bat

# Mac/Linux
chmod +x start_celery.sh
./start_celery.sh

# Or manually
python run_celery.py
```

The Celery worker will:
- Sync live matches every 5 minutes
- Sync scheduled matches (next 14 days) every 30 minutes
- Automatically retry failed tasks with exponential backoff

**Note**: Make sure Redis is running before starting Celery.

## API Endpoints

### Authentication
- `POST /v1/auth/signup` - Register new user
- `POST /v1/auth/login` - Login user

### Users
- `GET /v1/users/me` - Get current user profile

### Wallet
- `GET /v1/wallet` - Get wallet balance
- `GET /v1/wallet/transactions` - Get transaction history

### Matches
- `GET /v1/matches/today` - Get today's featured matches
- `GET /v1/matches/{id}` - Get match details

## Socket.IO Events

### Client → Server
- `join_room` - Join match room
- `leave_room` - Leave match room
- `send_message` - Send chat message
- `send_reaction` - Send camera reaction

### Server → Client
- `connected` - Connection established
- `room_joined` - Successfully joined room
- `new_message` - New chat message
- `new_reaction` - New camera reaction

## Database Models

- **User** - User accounts, KYC, roles
- **Wallet** - Virtual credits balance
- **Transaction** - Payment history
- **Match** - Live matches
- **MatchRoom** - User participation in matches
- **ChatMessage** - Chat messages and reactions

## Development

### Run Tests
```bash
pytest
```

### Format Code
```bash
black app/
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Use production database
3. Set strong secret keys
4. Use Gunicorn with Uvicorn workers:
```bash
gunicorn main:socket_app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:4000
```

## License

Proprietary
