#!/usr/bin/env python3
"""Script to fetch all real IDs from GanttPRO API for testing."""
import os
import sys
import time
import json
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BASE_URL = "https://api.ganttpro.com/v1.0"
API_KEY = os.getenv("API_KEY", "92dda54a62d5461e88a2924d55b749d0")

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def safe_request(method, url, **kwargs):
    """Make request with error handling."""
    try:
        response = requests.request(method, url, headers=headers, **kwargs)
        print(f"{method} {url} -> {response.status_code}")
        if response.status_code >= 400:
            print(f"  Error: {response.text[:200]}")
        return response
    except Exception as e:
        print(f"  Exception: {e}")
        return None


def fetch_ids():
    """Fetch all required IDs from API."""
    ids = {}
    
    # 1. Get USER_ID
    print("\n1. Fetching USER_ID...")
    response = safe_request("GET", f"{BASE_URL}/users")
    if response and response.status_code == 200:
        data = response.json()
        if data and isinstance(data, list) and len(data) > 0:
            ids['USER_ID'] = str(data[0].get('id', ''))
            print(f"   ✓ USER_ID: {ids['USER_ID']}")
    time.sleep(2)
    
    # 2. Get RESOURCE_ID and PROJECT_ID
    print("\n2. Fetching RESOURCE_ID and PROJECT_ID...")
    response = safe_request("GET", f"{BASE_URL}/resources")
    if response and response.status_code == 200:
        data = response.json()
        if data and isinstance(data, list) and len(data) > 0:
            first_resource = data[0]
            ids['RESOURCE_ID'] = str(first_resource.get('id', ''))
            # PROJECT_ID is nested in resourceProjects
            resource_projects = first_resource.get('resourceProjects', [])
            if resource_projects and len(resource_projects) > 0:
                ids['PROJECT_ID'] = str(resource_projects[0].get('projectId', ''))
            print(f"   ✓ RESOURCE_ID: {ids['RESOURCE_ID']}")
            print(f"   ✓ PROJECT_ID: {ids.get('PROJECT_ID', 'NOT FOUND')}")
    time.sleep(2)
    
    # 3. Get TASK_ID - try to create a task first
    print("\n3. Fetching/Creating TASK_ID...")
    if 'PROJECT_ID' in ids:
        # Try to get existing tasks first
        response = safe_request("GET", f"{BASE_URL}/tasks", params={"idProject": ids['PROJECT_ID']})
        if response and response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                ids['TASK_ID'] = str(data[0].get('id', ''))
                print(f"   ✓ TASK_ID (existing): {ids['TASK_ID']}")
            else:
                # Create a test task
                task_data = {
                    "idProject": int(ids['PROJECT_ID']),
                    "name": "Test Task for API Testing",
                    "start": "2024-01-01",
                    "finish": "2024-01-10",
                    "description": "Automatically created for API testing"
                }
                response = safe_request("POST", f"{BASE_URL}/tasks", json=task_data)
                if response and response.status_code in [200, 201]:
                    data = response.json()
                    ids['TASK_ID'] = str(data.get('id', ''))
                    print(f"   ✓ TASK_ID (created): {ids['TASK_ID']}")
    time.sleep(2)
    
    # 4. Get COMMENT_ID - create a comment on the task
    print("\n4. Fetching/Creating COMMENT_ID...")
    if 'TASK_ID' in ids:
        # Try to get existing comments
        response = safe_request("GET", f"{BASE_URL}/comments", params={"idTask": ids['TASK_ID']})
        if response and response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                ids['COMMENT_ID'] = str(data[0].get('id', ''))
                print(f"   ✓ COMMENT_ID (existing): {ids['COMMENT_ID']}")
            else:
                # Create a test comment
                comment_data = {
                    "idTask": int(ids['TASK_ID']),
                    "text": "Test comment for API testing"
                }
                response = safe_request("POST", f"{BASE_URL}/comments", json=comment_data)
                if response and response.status_code in [200, 201]:
                    data = response.json()
                    ids['COMMENT_ID'] = str(data.get('id', ''))
                    print(f"   ✓ COMMENT_ID (created): {ids['COMMENT_ID']}")
    time.sleep(2)
    
    # 5. Get TIMELOG_ID - create a timelog entry
    print("\n5. Fetching/Creating TIMELOG_ID...")
    if 'TASK_ID' in ids:
        # Try to get existing timelogs
        response = safe_request("GET", f"{BASE_URL}/timelogs", params={"idTask": ids['TASK_ID']})
        if response and response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                ids['TIMELOG_ID'] = str(data[0].get('id', ''))
                print(f"   ✓ TIMELOG_ID (existing): {ids['TIMELOG_ID']}")
            else:
                # Create a test timelog
                timelog_data = {
                    "idTask": int(ids['TASK_ID']),
                    "idResource": int(ids.get('RESOURCE_ID', 0)),
                    "date": "2024-01-01",
                    "time": 2.5,
                    "description": "Test timelog for API testing"
                }
                response = safe_request("POST", f"{BASE_URL}/timelogs", json=timelog_data)
                if response and response.status_code in [200, 201]:
                    data = response.json()
                    ids['TIMELOG_ID'] = str(data.get('id', ''))
                    print(f"   ✓ TIMELOG_ID (created): {ids['TIMELOG_ID']}")
    time.sleep(2)
    
    # 6. Get LINK_ID - create a link between tasks
    print("\n6. Fetching/Creating LINK_ID...")
    if 'TASK_ID' in ids and 'PROJECT_ID' in ids:
        # Try to get existing links
        response = safe_request("GET", f"{BASE_URL}/links", params={"idProject": ids['PROJECT_ID']})
        if response and response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                ids['LINK_ID'] = str(data[0].get('id', ''))
                print(f"   ✓ LINK_ID (existing): {ids['LINK_ID']}")
            else:
                # Need two tasks to create a link - create second task first
                task_data = {
                    "idProject": int(ids['PROJECT_ID']),
                    "name": "Second Test Task for Link",
                    "start": "2024-01-11",
                    "finish": "2024-01-20"
                }
                response2 = safe_request("POST", f"{BASE_URL}/tasks", json=task_data)
                if response2 and response2.status_code in [200, 201]:
                    task2_id = response2.json().get('id')
                    time.sleep(1)
                    
                    # Create link
                    link_data = {
                        "idProject": int(ids['PROJECT_ID']),
                        "source": int(ids['TASK_ID']),
                        "target": int(task2_id),
                        "type": 0  # finish-to-start
                    }
                    response = safe_request("POST", f"{BASE_URL}/links", json=link_data)
                    if response and response.status_code in [200, 201]:
                        data = response.json()
                        ids['LINK_ID'] = str(data.get('id', ''))
                        print(f"   ✓ LINK_ID (created): {ids['LINK_ID']}")
    time.sleep(2)
    
    # 7. Get ATTACHMENT_ID - note: might not be available in all API versions
    print("\n7. Fetching ATTACHMENT_ID...")
    if 'TASK_ID' in ids:
        response = safe_request("GET", f"{BASE_URL}/attachments", params={"idTask": ids['TASK_ID']})
        if response and response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                ids['ATTACHMENT_ID'] = str(data[0].get('id', ''))
                print(f"   ✓ ATTACHMENT_ID (existing): {ids['ATTACHMENT_ID']}")
            else:
                print(f"   ⚠ ATTACHMENT_ID: No attachments found (may need manual upload)")
        else:
            print(f"   ⚠ ATTACHMENT_ID: Endpoint not available or requires file upload")
    
    return ids


def update_env_file(ids):
    """Update .env file with fetched IDs."""
    env_path = ".env"
    
    # Read current .env content
    try:
        with open(env_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    
    # Update or add ID lines
    updated_lines = []
    keys_updated = set()
    
    for line in lines:
        updated = False
        for key, value in ids.items():
            if line.startswith(f"{key}="):
                updated_lines.append(f"{key}={value}\n")
                keys_updated.add(key)
                updated = True
                break
        if not updated:
            updated_lines.append(line)
    
    # Add missing keys
    for key, value in ids.items():
        if key not in keys_updated and value:
            updated_lines.append(f"{key}={value}\n")
    
    # Write back
    with open(env_path, 'w') as f:
        f.writelines(updated_lines)
    
    print(f"\n✓ Updated {env_path} with {len(ids)} IDs")


if __name__ == "__main__":
    print("=" * 60)
    print("GanttPRO API - Fetching Test IDs")
    print("=" * 60)
    
    ids = fetch_ids()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    for key, value in ids.items():
        status = "✓" if value else "✗"
        print(f"{status} {key}: {value if value else 'NOT FOUND'}")
    
    if ids:
        update_env_file(ids)
        print("\n✓ All available IDs have been saved to .env file")
    else:
        print("\n✗ No IDs were fetched successfully")
