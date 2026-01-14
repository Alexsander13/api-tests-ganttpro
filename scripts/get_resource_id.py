#!/usr/bin/env python3
"""
Script to fetch RESOURCE_ID from GanttPRO API
Run this locally to get your resource IDs for testing
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://api.ganttpro.com/v1.0")

if not API_KEY:
    print("❌ Error: API_KEY not found in .env file")
    print("Please set up .env file with API_KEY")
    exit(1)

print(f"📡 Fetching resources from {BASE_URL}...")
print(f"🔑 Using API Key: {API_KEY[:10]}...")
print("-" * 60)

headers = {
    "X-API-Key": API_KEY,
    "Accept": "application/json"
}

try:
    response = requests.get(f"{BASE_URL}/resources", headers=headers, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        
        # API returns list directly or wrapped in 'data' key
        resources = data if isinstance(data, list) else data.get('data', [])
        
        if resources:
            print(f"\n✅ Found {len(resources)} resource(s):\n")
            for resource in resources:
                resource_id = resource.get('id')
                name = resource.get('name', 'N/A')
                email = resource.get('email', 'N/A')
                print(f"  ID: {resource_id}")
                print(f"  Name: {name}")
                print(f"  Email: {email}")
                print()
            
            print("-" * 60)
            print("\n📋 Copy any ID above to use as RESOURCE_ID in GitHub Secrets")
            print(f"\nExample: RESOURCE_ID={resources[0].get('id')}")
        else:
            print("⚠️  No resources found in your account")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"❌ Connection error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
