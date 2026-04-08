# MatchHang Deployment Guide

Complete guide for deploying MatchHang to production.

## Prerequisites

- Ubuntu 20.04+ server
- Domain name (e.g., matchhang.com)
- SSL certificate (Let's Encrypt)
- PostgreSQL 14+
- Redis 6+
- Python 3.11+
- Node.js 18+
- Nginx

## 1. Server Setup

### Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### Install Dependencies
```bash
# Python
sudo apt install python3.11 python3.11-venv python3-pip -y

# Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Redis
sudo apt install redis-server -y

# Nginx
sudo apt install nginx -y

# Certbot (SSL)
sudo apt install certbot python3-certbot-nginx -y
```

## 2. Database Setup

### PostgreSQL
```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE matchhang;
CREATE USER matchhang_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE matchhang TO matchhang_user;
\q
```

### Redis
```bash
# Edit Redis config
sudo nano /etc/redis/redis.conf

# Set password
requirepass your_redis_password

# Restart Redis
sudo systemctl restart redis
sudo systemctl enable redis
```

## 3. Backend Deployment

### Clone Repository
```bash
cd /var/www
sudo git clone https://github.com/yourusername/matchhang.git
cd matchhang/backend
```

### Setup Python Environment
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configure Environment
```bash
cp .env.example .env
nano .env
```

Update `.env`:
```
DATABASE_URL=postgresql://matchhang_user:your_secure_password@localhost:5432/matchhang
REDIS_URL=redis://:your_redis_password@localhost:6379/0
SECRET_KEY=your_very_long_random_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
DEBUG=False
CORS_ORIGINS=https://matchhang.com,https://www.matchhang.com
```

### Run Migrations
```bash
alembic upgrade head
```

### Create Systemd Service
```bash
sudo nano /etc/systemd/system/matchhang-api.service
```

```ini
[Unit]
Description=MatchHang FastAPI Application
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/matchhang/backend
Environment="PATH=/var/www/matchhang/backend/venv/bin"
ExecStart=/var/www/matchhang/backend/venv/bin/uvicorn main:socket_app --host 0.0.0.0 --port 4000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start matchhang-api
sudo systemctl enable matchhang-api
```

## 4. Frontend Deployment

### Build Frontend
```bash
cd /var/www/matchhang/frontend
npm install
npm run build
```

### Configure Environment
```bash
nano .env.production
```

```
NEXT_PUBLIC_API_URL=https://api.matchhang.com
NEXT_PUBLIC_SOCKET_URL=https://api.matchhang.com
```

### Create Systemd Service
```bash
sudo nano /etc/systemd/system/matchhang-web.service
```

```ini
[Unit]
Description=MatchHang Next.js Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/matchhang/frontend
Environment="PATH=/usr/bin:/usr/local/bin"
Environment="NODE_ENV=production"
ExecStart=/usr/bin/npm start
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start matchhang-web
sudo systemctl enable matchhang-web
```

## 5. Nginx Configuration

### API Server
```bash
sudo nano /etc/nginx/sites-available/matchhang-api
```

```nginx
server {
    listen 80;
    server_name api.matchhang.com;

    location / {
        proxy_pass http://localhost:4000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Socket.IO
    location /socket.io {
        proxy_pass http://localhost:4000/socket.io;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Frontend
```bash
sudo nano /etc/nginx/sites-available/matchhang-web
```

```nginx
server {
    listen 80;
    server_name matchhang.com www.matchhang.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Enable Sites
```bash
sudo ln -s /etc/nginx/sites-available/matchhang-api /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/matchhang-web /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 6. SSL Certificates

```bash
# API
sudo certbot --nginx -d api.matchhang.com

# Frontend
sudo certbot --nginx -d matchhang.com -d www.matchhang.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

## 7. Firewall Setup

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 8. Monitoring & Logs

### View Logs
```bash
# API logs
sudo journalctl -u matchhang-api -f

# Frontend logs
sudo journalctl -u matchhang-web -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Setup Log Rotation
```bash
sudo nano /etc/logrotate.d/matchhang
```

```
/var/log/matchhang/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

## 9. Backup Strategy

### Database Backup
```bash
# Create backup script
sudo nano /usr/local/bin/backup-matchhang-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/matchhang"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

pg_dump -U matchhang_user matchhang | gzip > $BACKUP_DIR/matchhang_$DATE.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "matchhang_*.sql.gz" -mtime +7 -delete
```

```bash
sudo chmod +x /usr/local/bin/backup-matchhang-db.sh

# Add to crontab (daily at 2 AM)
sudo crontab -e
0 2 * * * /usr/local/bin/backup-matchhang-db.sh
```

## 10. Performance Optimization

### PostgreSQL Tuning
```bash
sudo nano /etc/postgresql/14/main/postgresql.conf
```

```
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB
max_connections = 200
```

### Redis Tuning
```bash
sudo nano /etc/redis/redis.conf
```

```
maxmemory 512mb
maxmemory-policy allkeys-lru
```

## 11. Security Checklist

- [ ] Change all default passwords
- [ ] Enable firewall (UFW)
- [ ] Setup SSL certificates
- [ ] Configure CORS properly
- [ ] Enable rate limiting
- [ ] Setup fail2ban
- [ ] Regular security updates
- [ ] Backup encryption
- [ ] Monitor logs for suspicious activity

## 12. Scaling

### Horizontal Scaling
- Use load balancer (Nginx/HAProxy)
- Multiple API servers
- Redis cluster
- PostgreSQL replication

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Add caching layers
- CDN for static assets

## 13. Monitoring Tools

### Install Monitoring
```bash
# Prometheus + Grafana
# PM2 for process management
npm install -g pm2

# Use PM2 instead of systemd
pm2 start /var/www/matchhang/backend/venv/bin/uvicorn --name matchhang-api -- main:socket_app --host 0.0.0.0 --port 4000
pm2 start npm --name matchhang-web -- start
pm2 save
pm2 startup
```

## 14. Troubleshooting

### API Not Starting
```bash
# Check logs
sudo journalctl -u matchhang-api -n 50

# Check if port is in use
sudo lsof -i :4000

# Test manually
cd /var/www/matchhang/backend
source venv/bin/activate
python main.py
```

### Database Connection Issues
```bash
# Test connection
psql -U matchhang_user -d matchhang -h localhost

# Check PostgreSQL status
sudo systemctl status postgresql
```

### Redis Connection Issues
```bash
# Test connection
redis-cli -a your_redis_password ping

# Check Redis status
sudo systemctl status redis
```

## 15. Maintenance

### Update Application
```bash
cd /var/www/matchhang
git pull origin main

# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart matchhang-api

# Frontend
cd ../frontend
npm install
npm run build
sudo systemctl restart matchhang-web
```

### Database Maintenance
```bash
# Vacuum database
sudo -u postgres psql matchhang -c "VACUUM ANALYZE;"

# Check database size
sudo -u postgres psql matchhang -c "SELECT pg_size_pretty(pg_database_size('matchhang'));"
```

## Support

For deployment issues:
- Check logs first
- Review configuration files
- Test components individually
- Contact support team

---

**MatchHang Production Deployment** 🚀
