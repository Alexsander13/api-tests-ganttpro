"""Test for creating task via POST /tasks"""
import pytest
import allure
from src.assertions import assert_status_code, assert_response_has_keys
from src.config import Config


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("positive")
def test_create_success(client, auth_headers, project_id):
    """Test successful task creation returns 200"""
    payload = {
        "projectId": int(project_id),
        "name": "Test Task Created via API"
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)
    
    assert_status_code(response, 200)
    # Check that response has item key with id
    data = response.json()
    assert "item" in data, "Response should have 'item' key"
    assert "id" in data["item"], "Task item should have 'id'"


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("auth")
def test_create_unauthorized(client, project_id):
    """Test task creation without API key returns 401"""
    payload = {
        "projectId": int(project_id),
        "name": "Test Task"
    }
    response = client.post("/tasks", json=payload, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("auth")
def test_create_invalid_key(client, project_id):
    """Test task creation with invalid API key returns 401"""
    payload = {
        "projectId": int(project_id),
        "name": "Test Task"
    }
    response = client.post("/tasks", json=payload, 
                          headers={"Accept": "application/json", "X-API-Key": "invalid_key_12345"})
    
    assert_status_code(response, 401)


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("validation")
def test_create_missing_name(client, auth_headers, project_id):
    """Test task creation without required name field returns 400"""
    payload = {
        "projectId": int(project_id)
        # Missing required 'name' field
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)
    
    assert_status_code(response, 400)


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("defaults")
def test_create_defaults(client, auth_headers, project_id):
    """Должны проставиться дефолты: status=1, progress=0, duration=1, type=task, color=1, estimation=0"""
    payload = {
        "projectId": int(project_id),
        "name": "Task defaults check"
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 200)
    item = response.json().get("item", {})
    assert item.get("status") == 1
    assert item.get("progress") in [0, 0.0]
    assert item.get("duration") == 1440  # API uses minutes (1 day = 1440 minutes)
    assert item.get("type") == "task"
    assert item.get("color") == 1
    assert item.get("estimation") in [0, 0.0]

    # cleanup
    if item.get("id"):
        try:
            client.delete(f"/tasks/{item['id']}", headers=auth_headers)
        except Exception:
            pass


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("logic")
def test_create_start_duration_calculates_end(client, auth_headers, project_id):
    """Если передали startDate и duration — endDate должен быть рассчитан"""
    payload = {
        "projectId": int(project_id),
        "name": "Task with start+duration",
        "startDate": "2025-01-10",
        "duration": 2
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 200)
    item = response.json().get("item", {})
    assert item.get("startDate").startswith("2025-01-10")  # API returns datetime format
    assert item.get("endDate") is not None
    assert item.get("duration") == 2

    if item.get("id"):
        try:
            client.delete(f"/tasks/{item['id']}", headers=auth_headers)
        except Exception:
            pass


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("logic")
def test_create_end_duration_calculates_start(client, auth_headers, project_id):
    """Если передали endDate и duration без startDate — startDate должен быть по умолчанию"""
    payload = {
        "projectId": int(project_id),
        "name": "Task with end+duration",
        "endDate": "2025-01-20",
        "duration": 3
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 200)
    item = response.json().get("item", {})
    assert item.get("endDate") is not None
    assert item.get("startDate") is not None
    assert item.get("duration") == 3

    if item.get("id"):
        try:
            client.delete(f"/tasks/{item['id']}", headers=auth_headers)
        except Exception:
            pass


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("validation")
def test_create_invalid_progress(client, auth_headers, project_id):
    """progress > 1 должно вернуть 400"""
    payload = {
        "projectId": int(project_id),
        "name": "Bad progress",
        "progress": 1.5
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 400)


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("validation")
def test_create_invalid_color(client, auth_headers, project_id):
    """color вне диапазона [1,18] должно вернуть 400"""
    payload = {
        "projectId": int(project_id),
        "name": "Bad color",
        "color": 19
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 400)


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("validation")
def test_create_missing_project_id(client, auth_headers):
    """Отсутствует projectId — ожидаем 400"""
    payload = {
        "name": "No project"
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 400)


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("logic")
def test_create_start_only_uses_default_duration(client, auth_headers, project_id):
    """Только startDate -> duration по умолчанию 1, endDate рассчитан"""
    payload = {
        "projectId": int(project_id),
        "name": "Start only",
        "startDate": "2025-01-05"
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 200)
    item = response.json().get("item", {})
    assert item.get("startDate").startswith("2025-01-05")  # API returns datetime format
    assert item.get("duration") == 1440  # Default duration in minutes
    assert item.get("endDate") is not None

    if item.get("id"):
        try:
            client.delete(f"/tasks/{item['id']}", headers=auth_headers)
        except Exception:
            pass


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("logic")
def test_create_duration_only_sets_dates(client, auth_headers, project_id):
    """Только duration -> startDate по умолчанию, endDate рассчитан"""
    payload = {
        "projectId": int(project_id),
        "name": "Duration only",
        "duration": 2
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 200)
    item = response.json().get("item", {})
    assert item.get("duration") == 2
    assert item.get("startDate") is not None
    assert item.get("endDate") is not None

    if item.get("id"):
        try:
            client.delete(f"/tasks/{item['id']}", headers=auth_headers)
        except Exception:
            pass


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("logic")
def test_create_all_dates_recalculates_end(client, auth_headers, project_id):
    """Переданы startDate, endDate и duration — endDate пересчитывается"""
    payload = {
        "projectId": int(project_id),
        "name": "Start+End+Duration",
        "startDate": "2025-01-10",
        "endDate": "2025-01-15",
        "duration": 4
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 200)
    item = response.json().get("item", {})
    assert item.get("startDate").startswith("2025-01-10")  # API returns datetime format
    assert item.get("duration") == 4
    assert item.get("endDate") is not None

    if item.get("id"):
        try:
            client.delete(f"/tasks/{item['id']}", headers=auth_headers)
        except Exception:
            pass


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("boundaries")
def test_create_progress_max_valid(client, auth_headers, project_id):
    """progress = 1 — граничное допустимое значение"""
    payload = {
        "projectId": int(project_id),
        "name": "Progress 1",
        "progress": 1
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 200)
    item = response.json().get("item", {})
    assert item.get("progress") in [1, 1.0]

    if item.get("id"):
        try:
            client.delete(f"/tasks/{item['id']}", headers=auth_headers)
        except Exception:
            pass


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("validation")
def test_create_progress_negative(client, auth_headers, project_id):
    """progress < 0 — ожидаем 400"""
    payload = {
        "projectId": int(project_id),
        "name": "Progress negative",
        "progress": -0.1
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 400)


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("boundaries")
def test_create_color_min_max(client, auth_headers, project_id):
    """color 1 и 18 — валидные границы"""
    payload1 = {"projectId": int(project_id), "name": "Color 1", "color": 1}
    payload2 = {"projectId": int(project_id), "name": "Color 18", "color": 18}

    resp1 = client.post("/tasks", json=payload1, headers=auth_headers)
    resp2 = client.post("/tasks", json=payload2, headers=auth_headers)

    assert_status_code(resp1, 200)
    assert_status_code(resp2, 200)

    for r in (resp1, resp2):
        item = r.json().get("item", {})
        if item.get("id"):
            try:
                client.delete(f"/tasks/{item['id']}", headers=auth_headers)
            except Exception:
                pass


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("validation")
def test_create_duration_zero(client, auth_headers, project_id):
    """duration=0 — ожидаем 400"""
    payload = {
        "projectId": int(project_id),
        "name": "Duration zero",
        "duration": 0
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 400)


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("validation")
def test_create_duration_negative(client, auth_headers, project_id):
    """duration<0 — ожидаем 400"""
    payload = {
        "projectId": int(project_id),
        "name": "Duration negative",
        "duration": -1
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 400)


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("edge-case")
def test_create_blank_name(client, auth_headers, project_id):
    """name из пробелов — API принимает (не валидирует)"""
    payload = {
        "projectId": int(project_id),
        "name": "   "
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 200)
    # API не валидирует пустое имя, создаёт таск
    item = response.json().get("item", {})
    assert item.get("name") == "   "
    
    if item.get("id"):
        try:
            client.delete(f"/tasks/{item['id']}", headers=auth_headers)
        except Exception:
            pass


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("features")
def test_create_with_parent(client, auth_headers, project_id, test_task_id):
    """Передан parent — должен сохраниться"""
    payload = {
        "projectId": int(project_id),
        "name": "Child task",
        "parent": int(test_task_id)
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 200)
    item = response.json().get("item", {})
    assert item.get("parent") == int(test_task_id)

    if item.get("id"):
        try:
            client.delete(f"/tasks/{item['id']}", headers=auth_headers)
        except Exception:
            pass


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("features")
def test_create_with_resources(client, auth_headers, project_id, resource_id):
    """Назначение ресурса при создании"""
    payload = {
        "projectId": int(project_id),
        "name": "Task with resource",
        "resources": [{"resourceId": int(resource_id), "resourceValue": 50}]
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 200)
    item = response.json().get("item", {})
    assert item.get("resources") is not None

    if item.get("id"):
        try:
            client.delete(f"/tasks/{item['id']}", headers=auth_headers)
        except Exception:
            pass


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("features")
def test_create_with_custom_field(client, auth_headers, project_id):
    """Передача customFields (если задан CUSTOM_FIELD_ID)"""
    custom_field_id = getattr(Config, "CUSTOM_FIELD_ID", None)
    if not custom_field_id:
        pytest.skip("CUSTOM_FIELD_ID не задан")

    payload = {
        "projectId": int(project_id),
        "name": "Task with CF",
        "customFields": [{"customFieldId": int(custom_field_id), "value": "abc"}]
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 200)
    item = response.json().get("item", {})
    assert item.get("customFields") is not None

    if item.get("id"):
        try:
            client.delete(f"/tasks/{item['id']}", headers=auth_headers)
        except Exception:
            pass


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("features")
def test_create_with_deadline(client, auth_headers, project_id):
    """Переданный deadline сохраняется (формат YYYY-MM-DD HH:mm)"""
    payload = {
        "projectId": int(project_id),
        "name": "Task with deadline",
        "deadline": "2025-02-01 15:00"
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 200)
    item = response.json().get("item", {})
    assert item.get("deadline") is not None
    assert "2025-02-01" in item.get("deadline", "")

    if item.get("id"):
        try:
            client.delete(f"/tasks/{item['id']}", headers=auth_headers)
        except Exception:
            pass


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("defaults")
def test_create_no_dates_sets_defaults(client, auth_headers, project_id):
    """Без startDate/endDate/duration должны выставиться дефолтные даты"""
    payload = {
        "projectId": int(project_id),
        "name": "No dates"
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 200)
    item = response.json().get("item", {})
    assert item.get("startDate") is not None
    assert item.get("endDate") is not None
    assert item.get("duration") == 1440  # Default duration in minutes

    if item.get("id"):
        try:
            client.delete(f"/tasks/{item['id']}", headers=auth_headers)
        except Exception:
            pass


@allure.feature("Tasks")
@allure.story("Create Task")
@allure.tag("POST")
@allure.tag("types")
def test_create_milestone_type(client, auth_headers, project_id):
    """type=milestone — поддерживается (task и milestone валидны)"""
    payload = {
        "projectId": int(project_id),
        "name": "Milestone type",
        "type": "milestone",
        "startDate": "2025-03-01"
    }
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert_status_code(response, 200)
    item = response.json().get("item", {})
    assert item.get("type") == "milestone"

    if item.get("id"):
        try:
            client.delete(f"/tasks/{item['id']}", headers=auth_headers)
        except Exception:
            pass
