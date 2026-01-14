#!/usr/bin/env python3
"""Script to fetch real IDs from GanttPRO API for testing."""
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
base_url = 'https://api.ganttpro.com/v1.0'
headers = {'X-API-Key': api_key, 'Accept': 'application/json'}

print('=== Получение данных из API GanttPRO ===\n')

results = {}

# Get USER_ID
try:
    print('Запрос пользователей...')
    r = requests.get(f'{base_url}/users', headers=headers)
    if r.status_code == 200:
        users = r.json()
        if users:
            results['USER_ID'] = users[0]['id']
            print(f'✓ USER_ID={results["USER_ID"]}')
        else:
            print('✗ Пользователи не найдены')
    else:
        print(f'✗ Ошибка при получении пользователей: {r.status_code}')
except Exception as e:
    print(f'✗ Ошибка: {e}')

time.sleep(2)

# Get RESOURCE_ID
try:
    print('\nЗапрос ресурсов...')
    r = requests.get(f'{base_url}/resources', headers=headers)
    if r.status_code == 200:
        resources = r.json()
        if resources:
            results['RESOURCE_ID'] = resources[0]['id']
            print(f'✓ RESOURCE_ID={results["RESOURCE_ID"]}')
        else:
            print('✗ Ресурсы не найдены')
    else:
        print(f'✗ Ошибка при получении ресурсов: {r.status_code}')
except Exception as e:
    print(f'✗ Ошибка: {e}')

time.sleep(2)

# Get PROJECT_ID from resources
try:
    print('\nПолучение PROJECT_ID из ресурсов...')
    r = requests.get(f'{base_url}/resources', headers=headers)
    if r.status_code == 200:
        resources = r.json()
        if resources and len(resources) > 0:
            for res in resources:
                if 'resourceProjects' in res and res['resourceProjects']:
                    results['PROJECT_ID'] = res['resourceProjects'][0]['projectId']
                    print(f'✓ PROJECT_ID={results["PROJECT_ID"]}')
                    break
            if 'PROJECT_ID' not in results:
                print('✗ Проекты не найдены в ресурсах')
        else:
            print('✗ Ресурсы пусты')
    else:
        print(f'✗ Ошибка: {r.status_code}')
except Exception as e:
    print(f'✗ Ошибка: {e}')

# Для остальных ID нужны реальные данные из проекта
print('\n' + '='*50)
print('\n📝 Результаты для .env файла:\n')
print('# Полученные ID из API:')
for key, value in results.items():
    print(f'{key}={value}')

print('\n# ID требуют создания тестовых данных:')
if 'PROJECT_ID' in results:
    print(f'TASK_ID=# Нужно создать задачу в проекте {results["PROJECT_ID"]}')
    print(f'COMMENT_ID=# Нужно создать комментарий')
    print(f'TIMELOG_ID=# Нужно создать time log')
    print(f'LINK_ID=# Нужно создать связь между задачами')
    print(f'ATTACHMENT_ID=# Нужно создать вложение')
else:
    print('TASK_ID=# Нет PROJECT_ID')
    print('COMMENT_ID=# Нет PROJECT_ID')
    print('TIMELOG_ID=# Нет PROJECT_ID')
    print('LINK_ID=# Нет PROJECT_ID')
    print('ATTACHMENT_ID=# Нет PROJECT_ID')

print('\n' + '='*50)
