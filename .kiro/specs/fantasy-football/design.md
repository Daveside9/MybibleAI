# Fantasy Football Design Document

## Overview

The fantasy football feature allows users to create virtual teams by selecting real football players within a budget constraint. Users earn points based on real match performance and can compete on leaderboards. This MVP focuses on core team building and scoring functionality.

## Architecture

### System Components

1. **Frontend (Next.js/React)**
   - Fantasy team builder interface
   - Player selection and filtering
   - Formation visualization
   - Points tracking dashboard

2. **Backend (FastAPI)**
   - Fantasy team CRUD operations
   - Player data management
   - Points calculation engine
   - Leaderboard generation

3. **Database (SQLite)**
   - Fantasy teams storage
   - Player statistics
   - User team associations

## Components and Interfaces

### Frontend Components

#### 1. FantasyPage (`/app/fantasy/page.tsx`)
- Main fantasy dashboard
- Displays team overview, budget, and points
- Shows pitch visualization with formation
- Handles team creation flow

#### 2. PlayerSelector Component
- Lists available players with filtering
- Shows player stats (position, team, cost, points)
- Allows player selection within budget
- Position-based filtering

#### 3. FormationView Component
- Visual pitch representation
- Displays players in formation (4-3-3, 4-4-2, etc.)
- Shows captain badge
- Interactive player positioning

#### 4. PointsTracker Component
- Displays total team points
- Shows individual player points breakdown
- Real-time updates during matches

### Backend Endpoints

#### Fantasy Team Endpoints

```python
GET    /api/v1/fantasy/team          # Get user's fantasy team
POST   /api/v1/fantasy/team          # Create fantasy team
PUT    /api/v1/fantasy/team          # Update fantasy team
DELETE /api/v1/fantasy/team          # Delete fantasy team

GET    /api/v1/fantasy/players       # Get available players
GET    /api/v1/fantasy/players/{id}  # Get player details
GET    /api/v1/fantasy/leaderboard   # Get leaderboard
```

## Data Models

### FantasyTeam Model

```python
class FantasyTeam(Base):
    __tablename__ = "fantasy_teams"
    
    id: int (PK)
    user_id: int (FK -> users.id)
    name: str
    formation: str  # "4-3-3", "4-4-2", etc.
    budget_remaining: float
    total_points: int
    captain_player_id: int (FK -> fantasy_players.id)
    created_at: datetime
    updated_at: datetime
```

### FantasyPlayer Model

```python
class FantasyPlayer(Base):
    __tablename__ = "fantasy_players"
    
    id: int (PK)
    name: str
    position: str  # "GK", "DEF", "MID", "FWD"
    team: str
    cost: float  # Player cost in fantasy coins
    points: int  # Total fantasy points
    goals: int
    assists: int
    clean_sheets: int
    created_at: datetime
    updated_at: datetime
```

### TeamPlayer Association

```python
class TeamPlayer(Base):
    __tablename__ = "team_players"
    
    id: int (PK)
    team_id: int (FK -> fantasy_teams.id)
    player_id: int (FK -> fantasy_players.id)
    is_captain: bool
    position_in_formation: int  # 1-11
    created_at: datetime
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Budget constraint enforcement
*For any* fantasy team creation or update, the total cost of all selected players must not exceed 100 coins
**Validates: Requirements 1.4**

### Property 2: Formation validity
*For any* selected formation, the number of players in each position must match the formation requirements (e.g., 4-3-3 requires 4 defenders, 3 midfielders, 3 forwards, and 1 goalkeeper)
**Validates: Requirements 2.1, 2.2**

### Property 3: Squad size constraint
*For any* fantasy team, the total number of players must equal exactly 11
**Validates: Requirements 1.3**

### Property 4: Captain points multiplier
*For any* fantasy team with a designated captain, the captain's points must be doubled in the total team score
**Validates: Requirements 2.5**

### Property 5: Points calculation accuracy
*For any* player performance (goals, assists, clean sheets), the fantasy points awarded must match the scoring rules (goals: 5 points, assists: 3 points, clean sheets: 4 points)
**Validates: Requirements 3.2, 3.3, 3.4**

## Error Handling

### Client-Side Errors
- Budget exceeded: Display remaining budget and prevent team save
- Invalid formation: Show formation requirements
- Network errors: Display retry option with error message
- Authentication errors: Redirect to login

### Server-Side Errors
- 400 Bad Request: Invalid team composition
- 401 Unauthorized: Missing or invalid authentication
- 404 Not Found: Team or player not found
- 500 Internal Server Error: Database or calculation errors

## Testing Strategy

### Unit Testing
- Test budget calculation logic
- Test formation validation
- Test points calculation for different scenarios
- Test player filtering and search

### Property-Based Testing
- Use Hypothesis (Python) for backend property tests
- Test budget constraints with random player selections
- Test formation validity with random formations
- Test points calculation with random match events
- Configure tests to run minimum 100 iterations

### Integration Testing
- Test complete team creation flow
- Test team update with player changes
- Test points calculation from match events
- Test leaderboard generation

## Implementation Notes

### Points Calculation
Points are calculated based on real match events:
- Goals: 5 points
- Assists: 3 points
- Clean sheets (GK/DEF): 4 points
- Captain bonus: 2x multiplier

### Formation Rules
Supported formations:
- 4-3-3: 1 GK, 4 DEF, 3 MID, 3 FWD
- 4-4-2: 1 GK, 4 DEF, 4 MID, 2 FWD
- 3-5-2: 1 GK, 3 DEF, 5 MID, 2 FWD
- 3-4-3: 1 GK, 3 DEF, 4 MID, 3 FWD

### Budget System
- Total budget: 100 coins
- Player costs range from 5-15 coins
- Budget must accommodate 11 players
- No transfers in MVP (future feature)
