#!/usr/bin/env python3
"""
Create Realistic Football Matches
Creates realistic match data for major leagues when API is not available
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.match import Match, Team, League, MatchStatus

# Real teams and leagues data
LEAGUES_DATA = {
    "Premier League": {
        "country": "England",
        "priority": 100,
        "teams": [
            "Arsenal", "Manchester City", "Liverpool", "Chelsea", "Manchester United",
            "Newcastle United", "Tottenham", "Brighton", "Aston Villa", "West Ham",
            "Crystal Palace", "Fulham", "Wolves", "Everton", "Brentford",
            "Nottingham Forest", "Luton Town", "Burnley", "Sheffield United", "Bournemouth"
        ]
    },
    "La Liga": {
        "country": "Spain", 
        "priority": 95,
        "teams": [
            "Real Madrid", "Barcelona", "Atletico Madrid", "Athletic Bilbao", "Real Sociedad",
            "Villarreal", "Valencia", "Sevilla", "Real Betis", "Osasuna",
            "Getafe", "Las Palmas", "Girona", "Alaves", "Mallorca",
            "Celta Vigo", "Cadiz", "Granada", "Almeria", "Rayo Vallecano"
        ]
    },
    "Serie A": {
        "country": "Italy",
        "priority": 90,
        "teams": [
            "Juventus", "AC Milan", "Inter Milan", "Napoli", "AS Roma",
            "Lazio", "Atalanta", "Fiorentina", "Bologna", "Torino",
            "Genoa", "Monza", "Lecce", "Udinese", "Cagliari",
            "Hellas Verona", "Empoli", "Frosinone", "Sassuolo", "Salernitana"
        ]
    },
    "UEFA Champions League": {
        "country": "Europe",
        "priority": 110,
        "teams": [
            "Manchester City", "Arsenal", "Real Madrid", "Barcelona", "Bayern Munich",
            "PSG", "Inter Milan", "Napoli", "Atletico Madrid", "Borussia Dortmund",
            "AC Milan", "Chelsea", "Liverpool", "Juventus", "Porto",
            "Benfica", "Ajax", "Shakhtar Donetsk", "RB Leipzig", "Sevilla"
        ]
    },
    "UEFA Europa League": {
        "country": "Europe",
        "priority": 75,
        "teams": [
            "West Ham", "Brighton", "Villarreal", "AS Roma", "Bayer Leverkusen",
            "Atalanta", "Marseille", "Eintracht Frankfurt", "Real Sociedad", "Ajax",
            "Freiburg", "Sporting CP", "Union Berlin", "Liverpool", "Toulouse",
            "Slavia Prague", "Qarabag", "Molde", "PAOK", "Sturm Graz"
        ]
    }
}

def create_realistic_odds():
    """Generate realistic betting odds"""
    # Generate odds that add up to roughly 100% (with bookmaker margin)
    home_prob = random.uniform(0.25, 0.55)  # 25-55% chance for home win
    draw_prob = random.uniform(0.20, 0.35)  # 20-35% chance for draw
    away_prob = 1.0 - home_prob - draw_prob
    
    # Convert probabilities to odds (with 5% margin)
    margin = 1.05
    home_odds = round((1 / home_prob) * margin, 2)
    draw_odds = round((1 / draw_prob) * margin, 2)
    away_odds = round((1 / away_prob) * margin, 2)
    
    return home_odds, draw_odds, away_odds

def get_match_status():
    """Get realistic match status distribution"""
    statuses = [
        (MatchStatus.SCHEDULED, 70),  # 70% scheduled
        (MatchStatus.LIVE, 5),        # 5% live
        (MatchStatus.FINISHED, 20),   # 20% finished
        (MatchStatus.POSTPONED, 3),   # 3% postponed
        (MatchStatus.CANCELLED, 2)    # 2% cancelled
    ]
    
    weights = [weight for _, weight in statuses]
    return random.choices([status for status, _ in statuses], weights=weights)[0]

def get_realistic_score(status):
    """Generate realistic scores based on match status"""
    if status == MatchStatus.FINISHED:
        # Finished matches have final scores
        home_score = random.choices([0, 1, 2, 3, 4, 5], weights=[15, 35, 30, 15, 4, 1])[0]
        away_score = random.choices([0, 1, 2, 3, 4], weights=[20, 40, 25, 10, 5])[0]
        return home_score, away_score
    elif status == MatchStatus.LIVE:
        # Live matches have current scores
        home_score = random.choices([0, 1, 2, 3], weights=[40, 35, 20, 5])[0]
        away_score = random.choices([0, 1, 2, 3], weights=[45, 35, 15, 5])[0]
        return home_score, away_score
    else:
        # Scheduled/postponed/cancelled matches have no scores
        return None, None

def create_leagues_and_teams(db):
    """Create leagues and teams in database"""
    print("🏆 Creating leagues and teams...")
    
    leagues = {}
    teams = {}
    
    for league_name, league_data in LEAGUES_DATA.items():
        # Create league
        league = League(
            name=league_name,
            country=league_data["country"],
            priority=league_data["priority"],
            external_id=random.randint(1000, 9999)  # Mock external ID
        )
        db.add(league)
        db.commit()
        db.refresh(league)
        leagues[league_name] = league
        
        print(f"   ✅ Created {league_name}")
        
        # Create teams for this league
        for team_name in league_data["teams"]:
            if team_name not in teams:  # Avoid duplicates (teams can be in multiple competitions)
                team = Team(
                    name=team_name,
                    external_id=random.randint(1000, 9999)  # Mock external ID
                )
                db.add(team)
                db.commit()
                db.refresh(team)
                teams[team_name] = team
    
    print(f"   ✅ Created {len(teams)} teams across {len(leagues)} leagues")
    return leagues, teams

def create_realistic_matches(db, leagues, teams, days_ahead=14):
    """Create realistic matches for the next few days"""
    print(f"⚽ Creating realistic matches for the next {days_ahead} days...")
    
    matches_created = 0
    today = datetime.now()
    
    for league_name, league in leagues.items():
        league_teams = LEAGUES_DATA[league_name]["teams"]
        
        # Create matches for each day
        for day_offset in range(days_ahead):
            match_date = today + timedelta(days=day_offset)
            
            # Determine number of matches for this day (more on weekends)
            if match_date.weekday() in [5, 6]:  # Saturday, Sunday
                num_matches = random.randint(3, 6)
            else:  # Weekdays
                num_matches = random.randint(1, 3)
            
            # Create matches for this day
            for _ in range(num_matches):
                # Pick random teams
                home_team_name = random.choice(league_teams)
                away_team_name = random.choice([t for t in league_teams if t != home_team_name])
                
                home_team = teams[home_team_name]
                away_team = teams[away_team_name]
                
                # Generate match time (typically 15:00, 17:30, 20:00)
                match_times = ["15:00", "17:30", "20:00", "12:30", "14:30"]
                match_time = random.choice(match_times)
                hour, minute = map(int, match_time.split(":"))
                
                scheduled_at = match_date.replace(
                    hour=hour, 
                    minute=minute, 
                    second=0, 
                    microsecond=0
                )
                
                # Generate match details
                status = get_match_status()
                home_score, away_score = get_realistic_score(status)
                home_odds, draw_odds, away_odds = create_realistic_odds()
                
                # Create match
                match = Match(
                    external_id=random.randint(100000, 999999),
                    title=f"{home_team_name} vs {away_team_name}",
                    home_team=home_team_name,
                    away_team=away_team_name,
                    home_team_id=home_team.id,
                    away_team_id=away_team.id,
                    league_id=league.id,
                    scheduled_at=scheduled_at,
                    status=status,
                    home_score=home_score,
                    away_score=away_score,
                    home_odds=home_odds,
                    away_odds=away_odds,
                    draw_odds=draw_odds,
                    is_featured=random.choice([True, False]),
                    last_synced=datetime.utcnow()
                )
                
                db.add(match)
                matches_created += 1
    
    db.commit()
    print(f"   ✅ Created {matches_created} realistic matches")
    return matches_created

def clear_existing_data(db):
    """Clear existing matches, teams, and leagues"""
    print("🧹 Clearing existing data...")
    
    # Delete in correct order (matches -> teams -> leagues)
    db.query(Match).delete()
    db.query(Team).delete()
    db.query(League).delete()
    db.commit()
    
    print("   ✅ Cleared existing data")

def main():
    """Main function"""
    print("🚀 Creating Realistic Football Matches")
    print("=" * 50)
    
    # Get database session
    db = next(get_db())
    
    try:
        # Clear existing data
        clear_existing_data(db)
        
        # Create leagues and teams
        leagues, teams = create_leagues_and_teams(db)
        
        # Create realistic matches
        matches_created = create_realistic_matches(db, leagues, teams)
        
        print(f"\n🎉 Successfully created:")
        print(f"   📊 {len(leagues)} leagues")
        print(f"   👥 {len(teams)} teams") 
        print(f"   ⚽ {matches_created} matches")
        print(f"\n✅ Your dashboard should now show realistic match data!")
        print(f"🔄 Refresh your browser to see the new matches.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()