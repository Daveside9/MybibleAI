#!/usr/bin/env python3
"""
Test script to debug fantasy team creation
"""
import requests
import json

API_URL = "http://localhost:4000"

def test_fantasy_creation():
    """Test the fantasy team creation process"""
    print("Testing fantasy team creation...")
    
    # First, try to login to get tokens
    login_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    try:
        # Login
        response = requests.post(f"{API_URL}/v1/auth/login", json=login_data)
        print(f"Login response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Login failed: {response.text}")
            return
            
        tokens = response.json()
        print("Login successful!")
        access_token = tokens["access_token"]
        
        # Test current user endpoint
        headers = {"Authorization": f"Bearer {access_token}"}
        user_response = requests.get(f"{API_URL}/v1/users/me", headers=headers)
        print(f"Current user response status: {user_response.status_code}")
        
        if user_response.status_code != 200:
            print(f"Current user failed: {user_response.text}")
            return
            
        user = user_response.json()
        print(f"Current user: {user['username']} (ID: {user['id']})")
        
        # Get fantasy players
        players_response = requests.get(f"{API_URL}/v1/fantasy/players", headers=headers)
        print(f"Players response status: {players_response.status_code}")
        
        if players_response.status_code != 200:
            print(f"Players failed: {players_response.text}")
            return
            
        players = players_response.json()
        print(f"Found {len(players)} players")
        
        # Select players that match 4-3-3 formation (1 GK, 4 DEF, 3 MID, 3 FWD)
        formation_requirements = {"GK": 1, "DEF": 4, "MID": 3, "FWD": 3}
        selected_players = []
        
        for position, count in formation_requirements.items():
            position_players = [p for p in players if p["position"] == position]
            if len(position_players) < count:
                print(f"Not enough {position} players. Need {count}, found {len(position_players)}")
                return
            selected_players.extend(position_players[:count])
        
        if len(selected_players) != 11:
            print(f"Could not select exactly 11 players. Got {len(selected_players)}")
            return
            
        player_ids = [p["id"] for p in selected_players]
        captain_id = player_ids[0]
        
        print(f"Selected players: {player_ids}")
        print(f"Captain: {captain_id}")
        
        # Count positions
        positions = {}
        for player in selected_players:
            pos = player["position"]
            positions[pos] = positions.get(pos, 0) + 1
            print(f"Player {player['id']}: {player['name']} ({pos}) - Cost: {player['cost']}")
        
        print(f"Position counts: {positions}")
        total_cost = sum(p["cost"] for p in selected_players)
        print(f"Total cost: {total_cost}")
        
        # Create team
        team_data = {
            "name": "Test Team",
            "formation": "4-3-3",
            "player_ids": player_ids,
            "captain_player_id": captain_id
        }
        
        print(f"Creating team with data: {team_data}")
        
        create_response = requests.post(f"{API_URL}/v1/fantasy/team", json=team_data, headers=headers)
        print(f"Create team response status: {create_response.status_code}")
        print(f"Create team response: {create_response.text}")
        
    except requests.exceptions.ConnectionError:
        print("Could not connect to API. Make sure the backend is running on localhost:4000")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_fantasy_creation()