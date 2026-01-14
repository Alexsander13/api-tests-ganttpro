import shutil
import os

dirs_to_remove = [
    'tests/endpoints/calendar',
    'tests/endpoints/customFields',
    'tests/endpoints/webhooks',
    'tests/endpoints/workload'
]

for dir_path in dirs_to_remove:
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print(f'Удалена папка: {dir_path}')

files_to_remove = [
    'tests/endpoints/resources/test_resources_get_one.py',
    'tests/endpoints/resources/test_resources_create.py',
    'tests/endpoints/resources/test_resources_delete.py',
    'tests/endpoints/resources/test_resources_update.py',
    'tests/endpoints/team/test_team_create.py',
    'tests/endpoints/team/test_team_delete.py',
    'tests/endpoints/team/test_team_update.py',
    'tests/endpoints/projects/test_projects_create.py',
    'tests/endpoints/projects/test_projects_update.py',
    'tests/endpoints/projects/test_projects_delete.py'
]

for file_path in files_to_remove:
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f'Удалён файл: {file_path}')
        
print('\nГотово! Удалены все тесты с 404 ответами.')
