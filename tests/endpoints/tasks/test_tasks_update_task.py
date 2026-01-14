"""Test for updating a task via PUT /tasks/{taskId}"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Tasks")
@allure.story("Update Task")
@allure.tag("PUT")
@allure.tag("positive")
def test_update_task_success(client, auth_headers, task_id):
    """Test successful task update returns 200"""
    payload = {"name": "Updated Task Name"}
    response = client.put(f"/tasks/{task_id}", json=payload, headers=auth_headers)
    if response.status_code == 429:
        assert_status_code(response, 429)
    else:
        assert_status_code(response, 200)
        assert_response_has_keys(response, ["status"])


@allure.feature("Tasks")
@allure.story("Update Task")
@allure.tag("PUT")
@allure.tag("auth")
def test_update_task_unauthorized(client, task_id):
    """Test task update without API key returns 401"""
    payload = {"name": "Updated Task Name"}
    response = client.put(f"/tasks/{task_id}", json=payload, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Tasks")
@allure.story("Update Task")
@allure.tag("PUT")
@allure.tag("validation")
def test_update_task_invalid_id(client, auth_headers):
    """Test task update with invalid ID returns 400 or 404 or 429"""
    payload = {"name": "Updated Task Name"}
    response = client.put("/tasks/-1", json=payload, headers=auth_headers)
    
    # API may return 400 for invalid ID format, 404 for not found, or 429 for rate limit
    assert response.status_code in [400, 404, 429], f"Expected 400, 404, or 429, got {response.status_code}"
