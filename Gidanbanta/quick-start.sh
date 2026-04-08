#!/bin/bash

# MatchHang Quick Start Script
# This script sets up the development environment

echo "🚀 MatchHang Quick Start"
echo "========================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

# Check if PostgreSQL is running
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL is not installed. You'll need to install it manually."
fi

# Check if Redis is running
if ! command -v redis-cli &> /dev/null; then
    echo "⚠️  Redis is not installed. You'll need to install it manually."
fi

echo "✅ Prerequisites check complete"
echo ""

# Setup Backend
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
echo "✅ Backend dependencies installed"

# Copy environment file
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ .env file created (please edit with your credentials)"
fi

cd ..

# Setup Frontend
echo ""
echo "📦 Setting up Frontend..."
cd frontend

# Install dependencies
npm install
echo "✅ Frontend dependencies installed"

# Copy environment file
if [ ! -f ".env.local" ]; then
    cp .env.local .env.local 2>/dev/null || echo "NEXT_PUBLIC_API_URL=http://localhost:4000
NEXT_PUBLIC_SOCKET_URL=http://localhost:4000
NEXT_PUBLIC_APP_NAME=MatchHang
NEXT_PUBLIC_CURRENCY_SYMBOL=₦
NEXT_PUBLIC_CHAT_UNLOCK_PRICE=100
NEXT_PUBLIC_FREE_MESSAGES_PER_MATCH=3" > .env.local
    echo "✅ .env.local file created"
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Setup PostgreSQL database:"
echo "   CREATE DATABASE matchhang;"
echo "   CREATE USER matchhang_user WITH PASSWORD 'your_password';"
echo "   GRANT ALL PRIVILEGES ON DATABASE matchhang TO matchhang_user;"
echo ""
echo "2. Update backend/.env with your database credentials"
echo ""
echo "3. Run database migrations:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   alembic upgrade head"
echo ""
echo "4. Start the backend:"
echo "   python main.py"
echo ""
echo "5. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "6. Visit http://localhost:3000"
echo ""
echo "🎉 Happy coding!"
