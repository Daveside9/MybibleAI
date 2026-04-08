#!/usr/bin/env python3
"""
Setup Leagues - Create proper leagues and associate matches with them
"""
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.match import Match, League

def setup_leagues():
    """Create leagues and associate matches with them"""
    
    db = SessionLocal()
    
    try:
        print("🏆 Setting Up Leagues...")
        print("=" * 50)
        
        # Create main leagues
        leagues_data = [
            {"name": "Premier League", "country": "England", "priority": 10, "external_id": 1001},
            {"name": "La Liga", "country": "Spain", "priority": 9, "external_id": 1002},
            {"name": "Serie A", "country": "Italy", "priority": 8, "external_id": 1003},
            {"name": "Bundesliga", "country": "Germany", "priority": 7, "external_id": 1004},
            {"name": "Ligue 1", "country": "France", "priority": 6, "external_id": 1005},
            {"name": "UEFA Champions League", "country": "Europe", "priority": 15, "external_id": 1006},
            {"name": "UEFA Europa League", "country": "Europe", "priority": 12, "external_id": 1007},
        ]
        
        created_leagues = {}
        
        for league_data in leagues_data:
            # Check if league exists
            existing = db.query(League).filter(League.name == league_data["name"]).first()
            
            if not existing:
                # Create new league
                league = League(
                    external_id=league_data["external_id"],
                    name=league_data["name"],
                    country=league_data["country"],
                    priority=league_data["priority"]
                )
                db.add(league)
                db.flush()  # Get the ID
                created_leagues[league_data["name"]] = league.id
                print(f"✅ Created: {league_data['name']} (ID: {league.id})")
            else:
                created_leagues[league_data["name"]] = existing.id
                print(f"📋 Exists: {league_data['name']} (ID: {existing.id})")
        
        # Associate matches with leagues based on their names
        matches = db.query(Match).filter(Match.external_id > 0).all()
        
        print(f"\n🔗 Associating {len(matches)} real matches with leagues...")
        
        updated_count = 0
        for match in matches:
            league_id = None
            
            # Determine league based on team names or existing data
            if any(team in match.title for team in ["Real Madrid", "Barcelona", "Atletico Madrid", "Valencia", "Sevilla", "Real Sociedad", "Girona"]):
                league_id = created_leagues.get("La Liga")
            elif any(team in match.title for team in ["Liverpool", "Chelsea", "Arsenal", "Manchester City", "Manchester United", "Tottenham"]):
                league_id = created_leagues.get("Premier League")
            elif any(team in match.title for team in ["Bayern Munich", "Dortmund", "RB Leipzig", "Union Berlin"]):
                league_id = created_leagues.get("Bundesliga")
            elif any(team in match.title for team in ["Juventus", "AC Milan", "Inter Milan", "Roma", "Napoli", "Lecce", "Pisa"]):
                league_id = created_leagues.get("Serie A")
            elif any(team in match.title for team in ["PSG", "Lyon", "Marseille", "Monaco", "Lille", "Nantes", "Angers"]):
                league_id = created_leagues.get("Ligue 1")
            else:
                # Default to Europa League for other matches
                league_id = created_leagues.get("UEFA Europa League")
            
            if league_id and match.league_id != league_id:
                match.league_id = league_id
                updated_count += 1
                league_name = next(name for name, id in created_leagues.items() if id == league_id)
                print(f"🔗 {match.title} → {league_name}")
        
        # Commit changes
        db.commit()
        
        print(f"\n✅ Leagues Setup Complete!")
        print(f"   • Created/Updated leagues: {len(leagues_data)}")
        print(f"   • Associated matches: {updated_count}")
        
        # Show league summary
        print(f"\n📊 League Summary:")
        for name, league_id in created_leagues.items():
            match_count = db.query(Match).filter(
                Match.league_id == league_id,
                Match.external_id > 0
            ).count()
            print(f"   🏆 {name}: {match_count} matches")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = setup_leagues()
    
    if success:
        print(f"\n🎬 Next Steps:")
        print(f"   1. Refresh your dashboard: http://localhost:3000/dashboard")
        print(f"   2. Click on league buttons to filter:")
        print(f"      • 'La Liga' - See Real Sociedad vs Girona")
        print(f"      • 'UEFA Europa League' - See Celtic vs AS Roma, FC Basel vs Aston Villa")
        print(f"      • 'Serie A' - See Lecce vs Pisa")
        print(f"      • 'Ligue 1' - See Angers vs Nantes")
        print(f"   3. Each league will show only its matches!")
    else:
        print(f"\n💥 Failed to setup leagues")