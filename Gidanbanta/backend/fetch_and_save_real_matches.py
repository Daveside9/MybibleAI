#!/usr/bin/env python3
"""
Fetch and Save Real Matches - Using Backend Environment
Works within the backend venv and uses the existing database setup
"""
import asyncio
import httpx
import sys
import os
from datetime import datetime, date, timedelta

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.match import Match, MatchStatus

async def fetch_real_matches_from_apis():
    """Fetch real matches from ESPN and other free APIs"""
    
    print("📺 Fetching Real Matches from APIs...")
    
    leagues = [
        ("eng.1", "Premier League"),
        ("esp.1", "La Liga"), 
        ("ger.1", "Bundesliga"),
        ("ita.1", "Serie A"),
        ("fra.1", "Ligue 1"),
        ("uefa.champions", "Champions League"),
        ("uefa.europa", "Europa League")
    ]
    
    all_matches = []
    
    async with httpx.AsyncClient() as client:
        for league_id, league_name in leagues:
            try:
                print(f"   Checking {league_name}...")
                response = await client.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/scoreboard")
                
                if response.status_code == 200:
                    data = response.json()
                    events = data.get("events", [])
                    league_matches = 0
                    
                    for event in events:
                        # Get match status
                        status = event.get("status", {}).get("type", {}).get("name", "")
                        
                        # Check if match is today, tomorrow, or live
                        event_date = event.get("date", "")
                        is_relevant = False
                        scheduled_at = None
                        
                        if event_date:
                            try:
                                match_datetime = datetime.fromisoformat(event_date.replace("Z", "+00:00"))
                                match_date = match_datetime.date()
                                today = date.today()
                                tomorrow = today + timedelta(days=1)
                                
                                # Include matches from today and tomorrow
                                if match_date in [today, tomorrow]:
                                    is_relevant = True
                                    scheduled_at = match_datetime
                            except:
                                pass
                        
                        # Always include live matches
                        if "IN_PROGRESS" in status or "HALFTIME" in status or "LIVE" in status:
                            is_relevant = True
                            if not scheduled_at:
                                scheduled_at = datetime.now()
                        
                        if is_relevant:
                            # Get team names and scores
                            competitions = event.get("competitions", [{}])
                            if competitions:
                                competitors = competitions[0].get("competitors", [])
                                if len(competitors) >= 2:
                                    home_team = competitors[0].get("team", {}).get("displayName", "")
                                    away_team = competitors[1].get("team", {}).get("displayName", "")
                                    home_score = int(competitors[0].get("score", 0))
                                    away_score = int(competitors[1].get("score", 0))
                                    
                                    # Map status
                                    our_status = MatchStatus.SCHEDULED
                                    if "IN_PROGRESS" in status or "HALFTIME" in status or "LIVE" in status:
                                        our_status = MatchStatus.LIVE
                                    elif "FINAL" in status or "FINISHED" in status:
                                        our_status = MatchStatus.FINISHED
                                    
                                    match_info = {
                                        "external_id": int(event.get("id", 0)),
                                        "title": f"{home_team} vs {away_team}",
                                        "home_team": home_team,
                                        "away_team": away_team,
                                        "home_score": home_score,
                                        "away_score": away_score,
                                        "status": our_status,
                                        "scheduled_at": scheduled_at,
                                        "league_name": league_name,
                                        "source": "ESPN"
                                    }
                                    
                                    all_matches.append(match_info)
                                    league_matches += 1
                    
                    if league_matches > 0:
                        print(f"     Found {league_matches} matches")
            
            except Exception as e:
                print(f"   ❌ Error fetching {league_name}: {e}")
    
    print(f"   Total matches found: {len(all_matches)}")
    return all_matches

def save_matches_to_database(matches):
    """Save matches to database using SQLAlchemy"""
    
    print(f"💾 Saving {len(matches)} matches to database...")
    
    db = SessionLocal()
    
    try:
        saved_count = 0
        updated_count = 0
        
        for match_data in matches:
            try:
                # Check if match already exists
                existing = db.query(Match).filter(
                    Match.external_id == match_data["external_id"]
                ).first()
                
                if existing:
                    # Update existing match
                    existing.home_score = match_data["home_score"]
                    existing.away_score = match_data["away_score"]
                    existing.status = match_data["status"]
                    existing.scheduled_at = match_data["scheduled_at"]
                    existing.is_featured = True
                    existing.stream_url = "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8"
                    
                    print(f"   🔄 Updated: {match_data['title']}")
                    updated_count += 1
                else:
                    # Create new match
                    new_match = Match(
                        external_id=match_data["external_id"],
                        title=match_data["title"],
                        home_team=match_data["home_team"],
                        away_team=match_data["away_team"],
                        home_score=match_data["home_score"],
                        away_score=match_data["away_score"],
                        status=match_data["status"],
                        scheduled_at=match_data["scheduled_at"],
                        is_featured=True,
                        stream_url="https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8",
                        home_odds=2.1,
                        away_odds=3.4,
                        draw_odds=3.2
                    )
                    
                    db.add(new_match)
                    print(f"   ➕ Added: {match_data['title']}")
                    saved_count += 1
                
                # Check if it's the Real Madrid vs Manchester City match
                if "Real Madrid" in match_data['title'] and "Manchester City" in match_data['title']:
                    print(f"   ⚽ FOUND: Real Madrid vs Manchester City!")
                    print(f"      Status: {match_data['status']}")
                    print(f"      Time: {match_data['scheduled_at']}")
                    print(f"      League: {match_data['league_name']}")
                
            except Exception as e:
                print(f"   ❌ Error processing {match_data['title']}: {e}")
        
        # Commit all changes
        db.commit()
        
        print(f"✅ Database updated successfully!")
        print(f"   • Added: {saved_count} new matches")
        print(f"   • Updated: {updated_count} existing matches")
        
        # Show summary
        live_count = db.query(Match).filter(Match.status == MatchStatus.LIVE).count()
        featured_count = db.query(Match).filter(Match.is_featured == True).count()
        total_count = db.query(Match).count()
        
        print(f"\n📊 Database Summary:")
        print(f"   • Live matches: {live_count}")
        print(f"   • Featured matches: {featured_count}")
        print(f"   • Total matches: {total_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

async def main():
    """Main function"""
    
    print("🔍 Fetching Real Live and Upcoming Matches")
    print("=" * 60)
    print(f"📅 Date: {date.today()}")
    print(f"🕘 Time: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    try:
        # Fetch matches from APIs
        matches = await fetch_real_matches_from_apis()
        
        if not matches:
            print("⏰ No matches found for today/tomorrow")
            print("💡 This could mean:")
            print("   • No matches scheduled for these dates")
            print("   • Try again during European match hours")
            return
        
        # Save to database
        success = save_matches_to_database(matches)
        
        if success:
            print(f"\n🎬 How to View Your Real Matches:")
            print(f"   1. Visit: http://localhost:3000/dashboard")
            print(f"   2. Click 'All Leagues' to see all matches")
            print(f"   3. Click '🔴 Live' to see live matches")
            print(f"   4. Look for Real Madrid vs Manchester City!")
            
            # Show featured matches
            real_madrid_matches = [m for m in matches if "Real Madrid" in m["title"]]
            city_matches = [m for m in matches if "Manchester City" in m["title"]]
            
            if real_madrid_matches or city_matches:
                print(f"\n⚽ Special Matches Found:")
                for match in real_madrid_matches + city_matches:
                    print(f"   🏆 {match['title']} - {match['status']} ({match['league_name']})")
        else:
            print(f"\n💥 Failed to save matches to database")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())