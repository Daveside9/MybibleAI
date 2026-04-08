"""
Performance Test Script
Test API endpoint response times
"""
import time
import requests
import json

API_URL = "http://localhost:4000"

def test_endpoint_performance():
    print("Testing API Performance...")
    print("=" * 50)
    
    # Test endpoints
    endpoints = [
        ("GET", "/v1/matches/1", "Get Match Details"),
        ("POST", "/v1/rooms/join/1", "Join Room"),
    ]
    
    # You'll need a valid token - get it from browser dev tools
    token = input("Enter your access token (from browser localStorage): ").strip()
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    for method, endpoint, description in endpoints:
        print(f"\n{description}:")
        print(f"{method} {endpoint}")
        
        start_time = time.time()
        
        try:
            if method == "GET":
                response = requests.get(f"{API_URL}{endpoint}", headers=headers)
            else:
                response = requests.post(f"{API_URL}{endpoint}", headers=headers)
            
            end_time = time.time()
            duration = (end_time - start_time) * 1000  # Convert to milliseconds
            
            print(f"Status: {response.status_code}")
            print(f"Time: {duration:.2f}ms")
            
            if response.status_code == 200:
                print("✅ Success")
            else:
                print(f"❌ Error: {response.text}")
                
        except Exception as e:
            end_time = time.time()
            duration = (end_time - start_time) * 1000
            print(f"❌ Exception: {e}")
            print(f"Time: {duration:.2f}ms")
        
        print("-" * 30)

if __name__ == "__main__":
    test_endpoint_performance()