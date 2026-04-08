#!/usr/bin/env python3
"""
Add more leagues to the database with proper external_id values
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.match import League
from sqlalchemy.orm import Session

def add_more_leagues():
    """Add popular football leagues to the database"""
    
    leagues_to_add = [
        # Major European Leagues
        {"id": 8, "external_id": 135, "name": "Serie A", "country": "Italy", "priority": 95},
        {"id": 9, "external_id": 78, "name": "Bundesliga", "country": "Germany", "priority": 94},
        {"id": 10, "external_id": 61, "name": "Ligue 1", "country": "France", "priority": 93},
        {"id": 11, "external_id": 88, "name": "Eredivisie", "country": "Netherlands", "priority": 85},
        {"id": 12, "external_id": 94, "name": "Primeira Liga", "country": "Portugal", "priority": 84},
        
        # International Competitions  
        {"id": 13, "external_id": 1001, "name": "UEFA Nations League", "country": "Europe", "priority": 90},
        {"id": 14, "external_id": 2000, "name": "FIFA World Cup", "country": "International", "priority": 100},
        
        # Other Popular Leagues
        {"id": 15, "external_id": 253, "name": "MLS", "country": "USA", "priority": 75},
        {"id": 16, "external_id": 262, "name": "Liga MX", "country": "Mexico", "priority": 74},
        {"id": 17, "external_id": 71, "name": "Brazilian Serie A", "country": "Brazil", "priority": 82},
        {"id": 18, "external_id": 128, "name": "Argentine Primera", "country": "Argentina", "priority": 81},
        
        # Additional European Leagues
        {"id": 19, "external_id": 144, "name": "Belgian Pro League", "country": "Belgium", "priority": 72},
        {"id": 20, "external_id": 207, "name": "Swiss Super League", "country": "Switzerland", "priority": 68},
        {"id": 21, "external_id": 218, "name": "Austrian Bundesliga", "country": "Austria", "priority": 67},
        {"id": 22, "external_id": 501, "name": "Scottish Premiership", "country": "Scotland", "priority": 71},
        {"id": 23, "external_id": 203, "name": "Turkish Super Lig", "country": "Turkey", "priority": 73},
        
        # African & Asian Leagues
        {"id": 24, "external_id": 3001, "name": "CAF Champions League", "country": "Africa", "priority": 78},
        {"id": 25, "external_id": 3002, "name": "AFCON", "country": "Africa", "priority": 87},
        {"id": 26, "external_id": 4001, "name": "AFC Champions League", "country": "Asia", "priority": 76},
        {"id": 27, "external_id": 302, "name": "J1 League", "country": "Japan", "priority": 70},
        {"id": 28, "external_id": 98, "name": "K League 1", "country": "South Korea", "priority": 69},
    ]
    
    db = next(get_db())
    
    try:
        print("Adding new leagues to database...")
        print("=" * 50)
        
        added_count = 0
        for league_data in leagues_to_add:
            # Check if league already exists
            existing = db.query(League).filter(League.id == league_data["id"]).first()
            if existing:
                print(f"League {league_data['name']} already exists, skipping...")
                continue
            
            # Create new league
            league = League(
                id=league_data["id"],
                external_id=league_data["external_id"],
                name=league_data["name"],
                country=league_data["country"],
                priority=league_data["priority"],
                logo=f"https://logos.api-sports.io/football/{league_data['external_id']}.png"
            )
            
            db.add(league)
            added_count += 1
            print(f"✅ Added: {league_data['name']} ({league_data['country']})")
        
        db.commit()
        print(f"\n🎉 Successfully added {added_count} new leagues!")
        
        # Show all leagues now
        print("\nAll leagues in database:")
        print("-" * 30)
        all_leagues = db.query(League).order_by(League.priority.desc()).all()
        for league in all_leagues:
            print(f"• {league.name} ({league.country}) - Priority: {league.priority}")
        
    except Exception as e:
        print(f"❌ Error adding leagues: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_more_leagues()