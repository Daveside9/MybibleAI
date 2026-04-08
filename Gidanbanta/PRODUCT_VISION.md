# MatchHang - Complete Product Vision

## 🎯 Core Concept
A Nigerian betting platform that combines:
- **Simple Betting** (Home/Away only)
- **Live Match Streaming** (viewing center experience)
- **Social Banter Chat** (monetized chat rooms)
- **Fantasy Football**
- **Wallet System** (Opay, PalmPay, Moniepoint)

---

## 🏠 Landing Page

### Design
- **Dark Blue Theme** (professional betting site aesthetic)
- **Hero Section**: Bold headline about betting + streaming + banter
- **Features Showcase**:
  - Simple betting (Home or Away)
  - Live streaming with chat
  - Nigerian viewing center experience
  - Fantasy football
- **Bonuses Section**:
  - Welcome bonus for new users
  - First deposit bonus
  - Referral bonuses
  - Free chat messages (3 per match)
- **How It Works**:
  1. Sign up & deposit
  2. Bet on matches (Home/Away)
  3. Watch live stream
  4. Banter in chat room (₦100/match)
- **Payment Partners**: Opay, PalmPay, Moniepoint logos
- **Call to Action**: "Start Betting Now" button

---

## 🎲 Betting System

### Betting Options
- **ONLY 2 OPTIONS**: Home Win OR Away Win
- **No Draw Option** (simplifies betting)
- **Minimum Bet**: ₦100
- **Maximum Bet**: ₦100,000 (configurable)

### Odds System
- Dynamic odds based on match data
- Company takes **5% commission** from total winnings
- Example:
  - User bets ₦1,000 on Chelsea (odds 2.0)
  - Chelsea wins → User gets ₦2,000
  - Company keeps ₦100 (5% of ₦2,000)

### Settlement Rules
1. **Win**: Full payout based on odds minus 5% commission
2. **Loss**: User loses bet amount
3. **Draw**: Automatic refund minus 5% processing fee
4. **Match Cancelled**: Full refund (no fee)

### Betting Flow
1. User sees today's matches on dashboard
2. Clicks match → sees betting slip
3. Selects Home or Away
4. Enters bet amount
5. Confirms bet (deducted from wallet)
6. Can now watch stream + chat (if paid ₦100)

---

## 📺 Live Streaming

### Stream Source
- **API Integration**: Use same provider as Bet9ja
  - Recommended: **SportRadar**, **IMG Arena**, or **Genius Sports**
  - These provide legal football streams with low latency
  - Requires licensing agreement

### Stream Features
- **HLS/DASH Player**: Adaptive bitrate streaming
- **Quality Options**: Auto, 720p, 480p, 360p
- **Low Latency**: <10 seconds delay
- **Picture-in-Picture**: Mobile support
- **Fullscreen Mode**
- **Match Stats Overlay**: Score, time, cards, substitutions

### Viewing Experience
- **Nigerian Viewing Center Style**:
  - Large video player (70% of screen on desktop)
  - Live score and match info always visible
  - Crowd reactions (emoji rain when goal scored)
  - Sound effects for goals, cards, etc.

---

## 💬 Chat Room (Banter Portal)

### Room Structure
- **Room Name**: "{Home Team} vs {Away Team} - Banta/Adawa"
- **Example**: "Chelsea vs Arsenal - Banta/Adawa"
- **Max Concurrent Matches**: 1-3 matches at a time
- **Room Lifecycle**: Opens 30 mins before match, closes 30 mins after

### Chat Access Model
- **Free Messages**: 3 messages per match (for all users)
- **Paid Access**: ₦100 per match for unlimited features
- **What ₦100 Unlocks**:
  - Unlimited text messages
  - Emoji reactions
  - 5-second video reactions (front camera)
  - Memes/GIF sharing
  - Voice notes (optional)

### Chat Features
1. **Text Messages**
   - Real-time messaging (Socket.IO)
   - User avatars and team badges
   - Message reactions (👍, 😂, 🔥, etc.)
   - Reply to messages

2. **5-Second Video Reactions**
   - Record from front camera
   - Auto-upload to cloud storage
   - Plays inline in chat
   - Auto-moderation for inappropriate content

3. **Emojis & Memes**
   - Football-themed emoji pack
   - Pre-approved meme library
   - No custom uploads (prevents abuse)

4. **Team Badges**
   - Users can select favorite team
   - Badge shows next to username
   - Creates rivalry atmosphere

### Moderation
- **AI Auto-Moderation**:
  - Profanity filter
  - Hate speech detection
  - Spam prevention
  - Inappropriate content blocking
- **Human Moderators**:
  - Review flagged content
  - Ban/mute abusive users
  - 24/7 coverage during matches
- **User Reports**: Flag button on messages
- **Banned Content**:
  - No advertisements
  - No external links
  - No personal attacks
  - No political/religious content
  - No nudity/violence

---

## 💰 Wallet System

### Wallet Structure
```
User Wallet
├── Deposited Balance (cannot withdraw)
├── Winnings Balance (can withdraw)
└── Total Balance (deposited + winnings)
```

### Deposit
- **Payment Methods**: Opay, PalmPay, Moniepoint
- **Minimum Deposit**: ₦500
- **Maximum Deposit**: ₦500,000 per transaction
- **Instant Credit**: Funds available immediately
- **No Deposit Fee**

### Withdrawal
- **Only Winnings**: Users can ONLY withdraw money they won
- **Deposited Money**: Must be used for betting (cannot withdraw)
- **Minimum Withdrawal**: ₦1,000
- **Maximum Withdrawal**: ₦1,000,000 per day
- **Processing Time**: 24-48 hours
- **Withdrawal Fee**: 2% (minimum ₦50)
- **KYC Required**: BVN verification for withdrawals

### Transaction Types
1. **Deposit** → Adds to deposited balance
2. **Bet Placed** → Deducts from total balance
3. **Bet Won** → Adds to winnings balance
4. **Bet Lost** → No action (already deducted)
5. **Chat Unlock** → Deducts ₦100 from total balance
6. **Withdrawal** → Deducts from winnings balance
7. **Refund** → Returns to deposited balance

### Payment Integration
- **Opay API**: Virtual account + transfer
- **PalmPay API**: QR code + transfer
- **Moniepoint API**: USSD + transfer
- **Webhook Verification**: Confirm all payments
- **Fraud Detection**: Flag suspicious transactions

---

## ⚽ Fantasy Football

### How Fantasy Football Works

#### Team Building
1. **Budget**: Each user gets ₦100M virtual budget
2. **Squad Selection**: Pick 11 players (any team)
   - 1 Goalkeeper
   - 3-5 Defenders
   - 3-5 Midfielders
   - 1-3 Forwards
3. **Player Prices**: Based on real performance
   - Top players: ₦15M-20M
   - Mid-tier: ₦8M-15M
   - Budget: ₦3M-8M
4. **Captain**: Choose 1 player (gets 2x points)

#### Scoring System
Players earn points based on real match performance:
- **Goal**: +6 points (forward), +8 (midfielder), +10 (defender/GK)
- **Assist**: +4 points
- **Clean Sheet**: +6 points (GK/defender), +2 (midfielder)
- **Yellow Card**: -2 points
- **Red Card**: -5 points
- **Own Goal**: -4 points
- **Penalty Save**: +8 points
- **Penalty Miss**: -4 points

#### Contests
1. **Free Leagues**:
   - No entry fee
   - Compete for bragging rights
   - Virtual trophies

2. **Paid Contests**:
   - Entry Fee: ₦200-₦5,000
   - Prize Pool: 90% of entries (10% to platform)
   - Top 30% win prizes
   - Example: ₦1,000 entry, 100 players
     - Prize Pool: ₦90,000
     - 1st: ₦30,000
     - 2nd: ₦20,000
     - 3rd: ₦10,000
     - 4th-10th: ₦3,000 each

3. **Weekly Leagues**:
   - Runs for entire matchweek
   - Can make transfers (1 free per week)
   - Leaderboard updates live

#### Transfers
- **Free Transfers**: 1 per week
- **Additional Transfers**: -4 points each
- **Wildcard**: Unlimited transfers (once per season)
- **Deadline**: 1 hour before first match

---

## 👤 User Dashboard (Bet9ja Style)

### Layout
```
┌─────────────────────────────────────────────────────────┐
│  HEADER: Logo | Matches | Streaming | Fantasy          │
│  RIGHT: [Wallet: ₦5,000] [Top Up] [Username] [Logout]  │
├─────────────────────────────────────────────────────────┤
│  SUB-HEADER: 3 Live Matches | Deposited: ₦10K | Wins   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  🔴 LIVE STREAMING NOW - Watch & Banter!                │
│  [Watch Now →]                                          │
│                                                          │
│  TODAY'S MATCHES                                        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ Chelsea      │ │ Man United   │ │ Arsenal      │   │
│  │ vs Arsenal   │ │ vs Liverpool │ │ vs Spurs     │   │
│  │ 🔴 LIVE      │ │ 3:00 PM      │ │ 5:30 PM      │   │
│  │ [Bet Now]    │ │ [Bet Now]    │ │ [Bet Now]    │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
│                                                          │
│  QUICK ACTIONS                                          │
│  [Fantasy Football] [My Bets] [Transactions]           │
└─────────────────────────────────────────────────────────┘
```

### Features
1. **Prominent Wallet**: Always visible in header
2. **Live Indicator**: Pulsing red dot for live matches
3. **Quick Bet**: One-click betting from dashboard
4. **Match Cards**: Show odds, time, teams
5. **Streaming Banner**: Highlighted at top when match is live

---

## 🎬 Match Room (Streaming + Chat)

### Layout
```
Desktop:
┌─────────────────────────────────────────────────────────┐
│  [← Back] Chelsea vs Arsenal - LIVE 🔴    [Wallet: ₦5K]│
├──────────────────────────────┬──────────────────────────┤
│                              │  CHAT ROOM               │
│                              │  ┌────────────────────┐  │
│      VIDEO PLAYER            │  │ User1: Goal! 🔥   │  │
│      (70% width)             │  │ User2: Penalty!   │  │
│                              │  │ [Video reaction]  │  │
│      [Score: 2-1]            │  └────────────────────┘  │
│      [Match Stats]           │                          │
│                              │  [Type message...]       │
│                              │  [😀] [📷] [Send]       │
└──────────────────────────────┴──────────────────────────┘

Mobile:
┌─────────────────────────────┐
│  VIDEO PLAYER (Full width)  │
│  [Score: 2-1]               │
├─────────────────────────────┤
│  CHAT (Scrollable)          │
│  User1: Goal! 🔥            │
│  User2: Penalty!            │
│  [Video reaction]           │
│                             │
│  [Type message...] [Send]   │
└─────────────────────────────┘
```

### Chat Unlock Flow
1. User enters match room
2. Can send 3 free messages
3. After 3rd message: "Unlock unlimited chat for ₦100"
4. User clicks "Unlock" → Payment modal
5. Deducts ₦100 from wallet
6. Full chat features unlocked for this match only

---

## 🔒 Security & Compliance

### Age Verification
- **18+ Only**: Betting is restricted to adults
- **BVN Verification**: Required for withdrawals
- **ID Upload**: Optional for higher limits

### Responsible Gambling
- **Deposit Limits**: Daily/weekly/monthly caps
- **Self-Exclusion**: Users can ban themselves
- **Reality Checks**: Popup after 2 hours
- **Loss Limits**: Set maximum loss per day

### Data Protection
- **Encryption**: All sensitive data encrypted
- **GDPR Compliance**: User data rights
- **Secure Payments**: PCI-DSS compliant
- **2FA**: Optional two-factor authentication

### Legal
- **Nigerian Gaming License**: Required
- **Terms & Conditions**: Clear betting rules
- **Privacy Policy**: Data handling transparency
- **Age Gate**: Verify 18+ before signup

---

## 📱 Technical Stack

### Frontend
- **Framework**: Next.js 14 (React + TypeScript)
- **Styling**: Tailwind CSS
- **State Management**: React Context + Zustand
- **Real-time**: Socket.IO Client
- **Video Player**: Video.js or HLS.js
- **Camera**: MediaRecorder API
- **Responsive**: Mobile-first design

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Real-time**: Socket.IO (python-socketio)
- **File Storage**: AWS S3 or Cloudinary
- **Queue**: Celery + Redis
- **Authentication**: JWT tokens

### Third-Party Services
- **Streaming API**: SportRadar / IMG Arena
- **Payment**: Opay, PalmPay, Moniepoint APIs
- **Moderation**: AWS Rekognition + Perspective API
- **SMS**: Termii or Africa's Talking
- **Email**: SendGrid or Mailgun

---

## 💵 Revenue Model

### Revenue Streams
1. **Betting Commission**: 5% of all winnings
2. **Chat Subscriptions**: ₦100 per match per user
3. **Fantasy Contests**: 10% of prize pools
4. **Withdrawal Fees**: 2% per withdrawal
5. **Premium Features** (future):
   - VIP chat badges
   - Exclusive emojis
   - Ad-free experience

### Projected Revenue (Example)
- **1,000 daily active users**
- **Average 2 bets per user**: ₦2,000/bet
- **50% chat unlock rate**: 500 users × ₦100 = ₦50,000
- **Betting commission**: 5% of ₦4M = ₦200,000
- **Daily Revenue**: ~₦250,000
- **Monthly Revenue**: ~₦7.5M

---

## 🚀 Development Phases

### Phase 1: MVP (8-10 weeks)
- [ ] Landing page with bonuses
- [ ] User authentication (signup/login)
- [ ] Wallet system (deposit/withdraw)
- [ ] Simple betting (Home/Away)
- [ ] Dashboard (Bet9ja style)
- [ ] Payment integration (Opay, PalmPay, Moniepoint)

### Phase 2: Streaming + Chat (6-8 weeks)
- [ ] Streaming API integration
- [ ] Match room with video player
- [ ] Real-time chat (Socket.IO)
- [ ] Chat unlock system (₦100)
- [ ] 5-second video reactions
- [ ] Emoji and meme support
- [ ] AI moderation

### Phase 3: Fantasy Football (4-6 weeks)
- [ ] Player database
- [ ] Team builder interface
- [ ] Scoring system
- [ ] Leagues and contests
- [ ] Live leaderboards
- [ ] Transfer system

### Phase 4: Polish & Scale (4-6 weeks)
- [ ] Mobile app (React Native)
- [ ] Advanced analytics
- [ ] Referral system
- [ ] Push notifications
- [ ] Performance optimization
- [ ] Load testing

---

## 📊 Success Metrics

### User Engagement
- Daily Active Users (DAU)
- Average bets per user
- Chat unlock conversion rate (target: 40%)
- Average watch time per match
- Fantasy participation rate

### Revenue
- Gross Gaming Revenue (GGR)
- Average Revenue Per User (ARPU)
- Chat subscription revenue
- Fantasy contest revenue
- Withdrawal rate (lower is better)

### Safety
- Moderation response time (<5 mins)
- False positive rate (<5%)
- User reports per 1000 messages (<2)
- Account verification rate (>80%)

---

## 🎯 Competitive Advantages

1. **Unique Combination**: Betting + Streaming + Social
2. **Simple Betting**: Only Home/Away (less confusing)
3. **Nigerian Focus**: Local payments, culture, language
4. **Viewing Center Experience**: Nostalgic, communal
5. **Monetized Chat**: New revenue stream
6. **Fantasy Football**: Additional engagement

---

**MatchHang** - Bet. Watch. Banter. Win! 🎉⚽💰
