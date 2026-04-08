"""
Create fantasy football tables in the database
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from app.core.database import engine, Base
from app.models.fantasy import FantasyPlayer, FantasyTeam, TeamPlayer
from app.models.user import User

def create_tables():
    """Create all fantasy tables"""
    print("Creating fantasy football tables...")
    
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Successfully created fantasy tables!")
        print("   - fantasy_players")
        print("   - fantasy_teams")
        print("   - team_players")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

if __name__ == "__main__":
    create_tables()
