"""
Create Test Matches
Populates the database with sample matches for testing the calendar view
"""
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.match import Match, Team, League, MatchStatus


def create_test_data():
    """Create test teams, leagues, and matches"""
    db = SessionLocal()
    
    try:
        # Create test leagues
        print("Creating leagues...")
        premier_league = League(
            external_id=39,
            name="Premier League",
            country="England",
            priority=100
        )
        la_liga = League(
            external_id=140,
            name="La Liga",
            country="Spain",
            priority=95
        )
        serie_a = League(
            external_id=135,
            name="Serie A",
            country="Italy",
            priority=90
        )
        
        db.add_all([premier_league, la_liga, serie_a])
        db.commit()
        db.refresh(premier_league)
        db.refresh(la_liga)
        db.refresh(serie_a)
        
        # Create test teams
        print("Creating teams...")
        teams_data = [
            (1, "Chelsea", "England"),
            (2, "Arsenal", "England"),
            (3, "Manchester United", "England"),
            (4, "Liverpool", "England"),
            (5, "Manchester City", "England"),
            (6, "Tottenham", "England"),
            (7, "Real Madrid", "Spain"),
            (8, "Barcelona", "Spain"),
            (9, "Atletico Madrid", "Spain"),
            (10, "AC Milan", "Italy"),
            (11, "Inter Milan", "Italy"),
            (12, "Juventus", "Italy"),
        ]
        
        teams = []
        for ext_id, name, country in teams_data:
            team = Team(
                external_id=ext_id,
                name=name,
                country=country
            )
            teams.append(team)
            db.add(team)
        
        db.commit()
        for team in teams:
            db.refresh(team)
        
        # Create test matches for the next 7 days
        print("Creating matches...")
        matches = []
        
        # Today's matches
        today = datetime.now().replace(hour=15, minute=0, second=0, microsecond=0)
        
        matches.append(Match(
            external_id=1001,
            title="Chelsea vs Arsenal",
            home_team="Chelsea",
            away_team="Arsenal",
            home_team_id=teams[0].id,
            away_team_id=teams[1].id,
            league_id=premier_league.id,
            scheduled_at=today,
            status=MatchStatus.SCHEDULED,
            home_odds=2.10,
            away_odds=3.20,
            draw_odds=3.40
        ))
        
        matches.append(Match(
            external_id=1002,
            title="Manchester United vs Liverpool",
            home_team="Manchester United",
            away_team="Liverpool",
            home_team_id=teams[2].id,
            away_team_id=teams[3].id,
            league_id=premier_league.id,
            scheduled_at=today + timedelta(hours=2),
            status=MatchStatus.SCHEDULED,
            home_odds=2.50,
            away_odds=2.80,
            draw_odds=3.10
        ))
        
        # Tomorrow's matches
        tomorrow = today + timedelta(days=1)
        
        matches.append(Match(
            external_id=1003,
            title="Real Madrid vs Barcelona",
            home_team="Real Madrid",
            away_team="Barcelona",
            home_team_id=teams[6].id,
            away_team_id=teams[7].id,
            league_id=la_liga.id,
            scheduled_at=tomorrow,
            status=MatchStatus.SCHEDULED,
            home_odds=2.20,
            away_odds=3.00,
            draw_odds=3.30
        ))
        
        matches.append(Match(
            external_id=1004,
            title="Manchester City vs Tottenham",
            home_team="Manchester City",
            away_team="Tottenham",
            home_team_id=teams[4].id,
            away_team_id=teams[5].id,
            league_id=premier_league.id,
            scheduled_at=tomorrow + timedelta(hours=3),
            status=MatchStatus.SCHEDULED,
            home_odds=1.60,
            away_odds=5.50,
            draw_odds=4.20
        ))
        
        # Day after tomorrow
        day_after = today + timedelta(days=2)
        
        matches.append(Match(
            external_id=1005,
            title="AC Milan vs Inter Milan",
            home_team="AC Milan",
            away_team="Inter Milan",
            home_team_id=teams[9].id,
            away_team_id=teams[10].id,
            league_id=serie_a.id,
            scheduled_at=day_after,
            status=MatchStatus.SCHEDULED,
            home_odds=2.40,
            away_odds=2.90,
            draw_odds=3.20
        ))
        
        matches.append(Match(
            external_id=1006,
            title="Atletico Madrid vs Real Madrid",
            home_team="Atletico Madrid",
            away_team="Real Madrid",
            home_team_id=teams[8].id,
            away_team_id=teams[6].id,
            league_id=la_liga.id,
            scheduled_at=day_after + timedelta(hours=2),
            status=MatchStatus.SCHEDULED,
            home_odds=3.10,
            away_odds=2.30,
            draw_odds=3.00
        ))
        
        # Add more matches for the next few days
        for i in range(3, 7):
            match_date = today + timedelta(days=i)
            
            matches.append(Match(
                external_id=1007 + i,
                title=f"{teams[i % 6].name} vs {teams[(i + 1) % 6].name}",
                home_team=teams[i % 6].name,
                away_team=teams[(i + 1) % 6].name,
                home_team_id=teams[i % 6].id,
                away_team_id=teams[(i + 1) % 6].id,
                league_id=premier_league.id if i % 2 == 0 else la_liga.id,
                scheduled_at=match_date,
                status=MatchStatus.SCHEDULED,
                home_odds=2.00 + (i * 0.1),
                away_odds=3.00 - (i * 0.1),
                draw_odds=3.20
            ))
        
        # Add one live match
        matches.append(Match(
            external_id=1020,
            title="Juventus vs AC Milan",
            home_team="Juventus",
            away_team="AC Milan",
            home_team_id=teams[11].id,
            away_team_id=teams[9].id,
            league_id=serie_a.id,
            scheduled_at=today - timedelta(minutes=30),
            status=MatchStatus.LIVE,
            home_score=1,
            away_score=1,
            home_odds=2.10,
            away_odds=3.40,
            draw_odds=3.10
        ))
        
        db.add_all(matches)
        db.commit()
        
        print(f"\n✅ Successfully created:")
        print(f"   - 3 leagues")
        print(f"   - {len(teams)} teams")
        print(f"   - {len(matches)} matches")
        print(f"\n🎉 Test data created! You can now view the calendar at http://localhost:3000/dashboard")
        
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_test_data()
