#!/usr/bin/env python3
"""
Debug Football API
Simple test to debug API connection issues
"""
import httpx
import asyncio
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

async def debug_api():
    """Debug API connection with detailed logging"""
    print("🔍 Debugging Football API connection...")
    
    # API details
    api_key = settings.FOOTBALL_API_KEY
    base_url = settings.FOOTBALL_API_BASE_URL
    rapidapi_host = settings.RAPIDAPI_HOST
    
    print(f"🔑 API Key: {api_key[:20]}...")
    print(f"🌐 Base URL: {base_url}")
    print(f"🏠 RapidAPI Host: {rapidapi_host}")
    
    # Headers
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": rapidapi_host
    }
    
    print(f"📋 Headers: {headers}")
    
    # Test endpoint
    url = f"{base_url}/status"
    
    print(f"\n🌐 Testing URL: {url}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📋 Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Response Data: {data}")
            else:
                print(f"❌ Error Response: {response.text}")
                
                # Try a different endpoint
                print("\n🔄 Trying leagues endpoint...")
                leagues_url = f"{base_url}/leagues"
                leagues_response = await client.get(leagues_url, headers=headers)
                
                print(f"📊 Leagues Status Code: {leagues_response.status_code}")
                print(f"❌ Leagues Error: {leagues_response.text}")
                
        except Exception as e:
            print(f"💥 Exception: {e}")

if __name__ == "__main__":
    asyncio.run(debug_api())