"""
Seed fantasy players from existing match data
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.fantasy import FantasyPlayer
from app.models.match import Match
import random

# Sample players data
SAMPLE_PLAYERS = [
    # Goalkeepers
    {"name": "Alisson Becker", "position": "GK", "team": "Liverpool", "cost": 12.0},
    {"name": "Ederson", "position": "GK", "team": "Manchester City", "cost": 11.5},
    {"name": "David Raya", "position": "GK", "team": "Arsenal", "cost": 10.5},
    {"name": "Andre Onana", "position": "GK", "team": "Manchester United", "cost": 10.0},
    
    # Defenders
    {"name": "Virgil van Dijk", "position": "DEF", "team": "Liverpool", "cost": 13.0},
    {"name": "William Saliba", "position": "DEF", "team": "Arsenal", "cost": 12.5},
    {"name": "Ruben Dias", "position": "DEF", "team": "Manchester City", "cost": 12.0},
    {"name": "Gabriel Magalhaes", "position": "DEF", "team": "Arsenal", "cost": 11.5},
    {"name": "Trent Alexander-Arnold", "position": "DEF", "team": "Liverpool", "cost": 14.0},
    {"name": "Kyle Walker", "position": "DEF", "team": "Manchester City", "cost": 11.0},
    {"name": "Lisandro Martinez", "position": "DEF", "team": "Manchester United", "cost": 10.5},
    {"name": "Ben White", "position": "DEF", "team": "Arsenal", "cost": 11.0},
    
    # Midfielders
    {"name": "Kevin De Bruyne", "position": "MID", "team": "Manchester City", "cost": 15.0},
    {"name": "Bruno Fernandes", "position": "MID", "team": "Manchester United", "cost": 13.5},
    {"name": "Martin Odegaard", "position": "MID", "team": "Arsenal", "cost": 13.0},
    {"name": "Mohamed Salah", "position": "MID", "team": "Liverpool", "cost": 14.5},
    {"name": "Phil Foden", "position": "MID", "team": "Manchester City", "cost": 13.5},
    {"name": "Bukayo Saka", "position": "MID", "team": "Arsenal", "cost": 13.0},
    {"name": "Alexis Mac Allister", "position": "MID", "team": "Liverpool", "cost": 11.5},
    {"name": "Bernardo Silva", "position": "MID", "team": "Manchester City", "cost": 12.5},
    
    # Forwards
    {"name": "Erling Haaland", "position": "FWD", "team": "Manchester City", "cost": 15.0},
    {"name": "Darwin Nunez", "position": "FWD", "team": "Liverpool", "cost": 12.0},
    {"name": "Gabriel Jesus", "position": "FWD", "team": "Arsenal", "cost": 11.5},
    {"name": "Marcus Rashford", "position": "FWD", "team": "Manchester United", "cost": 12.5},
    {"name": "Julian Alvarez", "position": "FWD", "team": "Manchester City", "cost": 11.0},
    {"name": "Kai Havertz", "position": "FWD", "team": "Arsenal", "cost": 10.5},
    {"name": "Rasmus Hojlund", "position": "FWD", "team": "Manchester United", "cost": 10.0},
    {"name": "Luis Diaz", "position": "FWD", "team": "Liverpool", "cost": 11.5},
]


def seed_fantasy_players(db: Session):
    """Seed fantasy players into database"""
    print("Seeding fantasy players...")
    
    # Check if players already exist
    existing_count = db.query(FantasyPlayer).count()
    if existing_count > 0:
        print(f"Found {existing_count} existing players. Skipping seed.")
        return
    
    # Add sample players
    for player_data in SAMPLE_PLAYERS:
        player = FantasyPlayer(
            name=player_data["name"],
            position=player_data["position"],
            team=player_data["team"],
            cost=player_data["cost"],
            points=random.randint(0, 50),  # Random initial points
            goals=random.randint(0, 10),
            assists=random.randint(0, 8),
            clean_sheets=random.randint(0, 5) if player_data["position"] in ["GK", "DEF"] else 0
        )
        db.add(player)
    
    db.commit()
    print(f"Successfully seeded {len(SAMPLE_PLAYERS)} fantasy players!")


def main():
    db = SessionLocal()
    try:
        seed_fantasy_players(db)
    except Exception as e:
        print(f"Error seeding players: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
