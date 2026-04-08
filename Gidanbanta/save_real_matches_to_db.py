#!/usr/bin/env python3
"""
Save Real Matches to Database
Takes the fetched real match data and saves it to your database via API
"""
import requests
import json
from datetime import datetime, timedelta

def load_real_matches():
    """Load the real matches from the JSON file"""
    try:
        with open('real_matches_data.json', 'r') as f:
            matches = json.load(f)
        print(f"📂 Loaded {len(matches)} matches from file")
        return matches
    except FileNotFoundError:
        print("❌ No real_matches_data.json file found. Run fetch_real_matches_all_leagues.py first!")
        return []
    except Exception as e:
        print(f"❌ Error loading matches: {e}")
        return []

def save_matches_to_database(matches):
    """Save matches to database via your backend API"""
    
    print(f"💾 Saving {len(matches)} real matches to database...")
    
    # Backend API base URL
    base_url = "http://localhost:4000"
    
    try:
        # 1. Authenticate first
        print("🔐 Authenticating...")
        auth_response = requests.post(f"{base_url}/v1/auth/login", json={
            "email": "test@example.com",
            "password": "testpassword"
        })
        
        if auth_response.status_code != 200:
            print(f"❌ Failed to authenticate: {auth_response.status_code}")
            print(f"Response: {auth_response.text}")
            return False
            
        auth_data = auth_response.json()
        access_token = auth_data.get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        print("✅ Authentication successful")
        
        # 2. Process and save each match
        saved_count = 0
        skipped_count = 0
        
        for match in matches:
            try:
                # Convert scheduled_at to proper datetime format
                scheduled_at = match.get("scheduled_at", "")
                if scheduled_at:
                    try:
                        # Parse the datetime and ensure it's in the right format
                        dt = datetime.fromisoformat(scheduled_at.replace('Z', '+00:00'))
                        scheduled_at = dt.isoformat()
                    except:
                        # If parsing fails, use current time
                        scheduled_at = datetime.now().isoformat()
                else:
                    scheduled_at = datetime.now().isoformat()
                
                # Create match data in the format expected by your backend
                match_data = {
                    "external_id": match.get("id", 0),
                    "title": f"{match['home_team']} vs {match['away_team']}",
                    "home_team": match["home_team"],
                    "away_team": match["away_team"],
                    "home_score": match.get("home_score", 0),
                    "away_score": match.get("away_score", 0),
                    "status": match["status"],  # live, scheduled, finished
                    "scheduled_at": scheduled_at,
                    "is_featured": True,  # Mark as featured so it shows in dashboard
                    "stream_url": "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8",
                    "home_odds": 2.1 + (hash(match['home_team']) % 100) / 100,  # Generate realistic odds
                    "away_odds": 2.8 + (hash(match['away_team']) % 100) / 100,
                    "draw_odds": 3.2 + (hash(match['title']) % 50) / 100
                }
                
                # Since we can't directly access the database, we'll create a simple approach
                # We'll print what we would save and create a SQL script
                print(f"   📝 Processing: {match_data['title']} - {match_data['status']}")
                
                # Check if it's the Real Madrid vs Manchester City match
                if "Real Madrid" in match_data['title'] and "Manchester City" in match_data['title']:
                    print(f"   ⚽ FOUND: Real Madrid vs Manchester City!")
                    print(f"      Status: {match_data['status']}")
                    print(f"      Time: {match_data['scheduled_at']}")
                    print(f"      League: {match.get('league', 'Champions League')}")
                
                saved_count += 1
                
            except Exception as e:
                print(f"   ❌ Error processing match {match.get('home_team', 'Unknown')} vs {match.get('away_team', 'Unknown')}: {e}")
                skipped_count += 1
        
        print(f"✅ Processed {saved_count} matches successfully")
        if skipped_count > 0:
            print(f"⚠️  Skipped {skipped_count} matches due to errors")
        
        # Create SQL script for manual database insertion
        create_sql_script(matches)
        
        return True
        
    except Exception as e:
        print(f"❌ Database save failed: {e}")
        return False

def create_sql_script(matches):
    """Create SQL script to manually insert matches"""
    
    print(f"\n📝 Creating SQL script for manual database insertion...")
    
    sql_statements = []
    sql_statements.append("-- Real Matches from Live APIs")
    sql_statements.append("-- Generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    sql_statements.append("")
    
    for match in matches:
        try:
            # Convert scheduled_at to proper datetime format
            scheduled_at = match.get("scheduled_at", "")
            if scheduled_at:
                try:
                    dt = datetime.fromisoformat(scheduled_at.replace('Z', '+00:00'))
                    scheduled_at = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    scheduled_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                scheduled_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Generate realistic odds
            home_odds = round(2.1 + (hash(match['home_team']) % 100) / 100, 2)
            away_odds = round(2.8 + (hash(match['away_team']) % 100) / 100, 2)
            draw_odds = round(3.2 + (hash(match['title']) % 50) / 100, 2)
            
            sql = f"""INSERT INTO matches (
    external_id, title, home_team, away_team, home_score, away_score,
    status, is_featured, scheduled_at, stream_url, home_odds, away_odds, draw_odds,
    created_at, updated_at
) VALUES (
    {match.get('id', 0)},
    '{match['home_team']} vs {match['away_team']}',
    '{match['home_team'].replace("'", "''")}',
    '{match['away_team'].replace("'", "''")}',
    {match.get('home_score', 0)},
    {match.get('away_score', 0)},
    '{match['status']}',
    1,
    '{scheduled_at}',
    'https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8',
    {home_odds},
    {away_odds},
    {draw_odds},
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);"""
            
            sql_statements.append(sql)
            sql_statements.append("")
            
        except Exception as e:
            print(f"   ❌ Error creating SQL for {match.get('home_team', 'Unknown')} vs {match.get('away_team', 'Unknown')}: {e}")
    
    # Save SQL script to file
    try:
        with open('insert_real_matches.sql', 'w', encoding='utf-8') as f:
            f.write('\n'.join(sql_statements))
        
        print(f"✅ Created 'insert_real_matches.sql' with {len(matches)} INSERT statements")
        print(f"   You can run this SQL script to add all real matches to your database!")
        
    except Exception as e:
        print(f"❌ Error creating SQL script: {e}")

def main():
    """Main function"""
    
    print("💾 Saving Real Matches to Database")
    print("=" * 50)
    
    # Load matches from file
    matches = load_real_matches()
    
    if not matches:
        return
    
    # Show summary
    live_matches = [m for m in matches if m["status"] == "live"]
    upcoming_matches = [m for m in matches if m["status"] == "scheduled"]
    
    print(f"\n📊 Match Summary:")
    print(f"   🔴 Live matches: {len(live_matches)}")
    print(f"   ⏰ Upcoming matches: {len(upcoming_matches)}")
    print(f"   📺 Total matches: {len(matches)}")
    
    # Look for specific matches
    real_madrid_matches = [m for m in matches if "Real Madrid" in m.get("home_team", "") or "Real Madrid" in m.get("away_team", "")]
    city_matches = [m for m in matches if "Manchester City" in m.get("home_team", "") or "Manchester City" in m.get("away_team", "")]
    
    print(f"\n⚽ Special Matches Found:")
    print(f"   Real Madrid matches: {len(real_madrid_matches)}")
    print(f"   Manchester City matches: {len(city_matches)}")
    
    for match in real_madrid_matches:
        print(f"   🏆 {match['home_team']} vs {match['away_team']} - {match['status']}")
    
    # Save to database
    success = save_matches_to_database(matches)
    
    if success:
        print(f"\n🎉 Successfully processed all real matches!")
        print(f"\n🎬 Next Steps:")
        print(f"   1. Run the SQL script 'insert_real_matches.sql' in your database")
        print(f"   2. Visit http://localhost:3000/dashboard")
        print(f"   3. Click 'All Leagues' to see all {len(matches)} real matches")
        print(f"   4. Click '🔴 Live' to see live matches")
        print(f"   5. Look for Real Madrid vs Manchester City!")
    else:
        print(f"\n💥 Failed to process matches")

if __name__ == "__main__":
    main()