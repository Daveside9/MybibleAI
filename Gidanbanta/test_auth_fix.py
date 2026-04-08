#!/usr/bin/env python3
"""
Test script to verify authentication fix
"""
import requests
import json

API_URL = "http://localhost:4000"

def test_refresh_token():
    """Test the refresh token endpoint"""
    print("Testing refresh token endpoint...")
    
    # First, try to login to get tokens
    login_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    try:
        response = requests.post(f"{API_URL}/v1/auth/login", json=login_data)
        print(f"Login response status: {response.status_code}")
        
        if response.status_code == 200:
            tokens = response.json()
            print("Login successful!")
            
            # Test refresh token
            refresh_data = {
                "refresh_token": tokens["refresh_token"]
            }
            
            refresh_response = requests.post(f"{API_URL}/v1/auth/refresh", json=refresh_data)
            print(f"Refresh response status: {refresh_response.status_code}")
            
            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                print("Refresh successful!")
                print(f"New access token: {new_tokens['access_token'][:50]}...")
            else:
                print(f"Refresh failed: {refresh_response.text}")
        else:
            print(f"Login failed: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Could not connect to API. Make sure the backend is running on localhost:4000")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_refresh_token()