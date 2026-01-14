import sys
import json
sys.path.insert(0, '.')
from src.config import Config
from src.http_client import HTTPClient

client = HTTPClient(base_url=Config.BASE_URL)
headers = Config.get_auth_headers()
project_id = Config.PROJECT_ID

# Create a task for link
task_data = {'projectId': int(project_id), 'name': 'Link test task', 'description': 'Test'}
response = client.post('/tasks', headers=headers, json=task_data)
task1_id = response.json().get('item', {}).get('id')
print(f'Task 1 ID: {task1_id}')

# Create second task
response = client.post('/tasks', headers=headers, json=task_data)
task2_id = response.json().get('item', {}).get('id')
print(f'Task 2 ID: {task2_id}')

# Create link
link_data = {'projectId': int(project_id), 'source': int(task1_id), 'target': int(task2_id), 'type': 0}
response = client.post('/links', headers=headers, json=link_data)
print(f'Link response status: {response.status_code}')
print(f'Link response: {json.dumps(response.json(), indent=2)}')
link_id = response.json().get('item', {}).get('id')
print(f'Link ID extracted: {link_id}')

# Test timelog
timelog_data = {'taskId': int(task1_id), 'resourceId': int(Config.RESOURCE_ID), 'date': '2024-01-15', 'time': 4.0}
response = client.post('/timeLogs', headers=headers, json=timelog_data)
print(f'\nTimelog response status: {response.status_code}')
print(f'Timelog response: {json.dumps(response.json(), indent=2)}')
timelog_id = response.json().get('item', {}).get('id')
print(f'Timelog ID extracted: {timelog_id}')
