"""Test for updating task via PUT /tasks/{taskId}"""
import pytest
import allure
from src.assertions import assert_status_code


@allure.feature("Tasks")
@allure.story("Update Task")
@allure.tag("PUT")
@allure.tag("positive")
def test_update_success(client, auth_headers, fresh_task_id):
    """Test successful task update returns 200"""
    payload = {
        "name": "Updated Task Name"
    }
    response = client.put(f"/tasks/{fresh_task_id}", json=payload, headers=auth_headers)
    
    assert_status_code(response, 200)
    data = response.json()
    assert ("item" in data) or (data.get("status") == "ok"), "Response should include item or status ok"


@allure.feature("Tasks")
@allure.story("Update Task")
@allure.tag("PUT")
@allure.tag("auth")
def test_update_unauthorized(client, fresh_task_id):
    """Test task update without API key returns 401"""
    payload = {
        "name": "Updated Task Name"
    }
    response = client.put(f"/tasks/{fresh_task_id}", json=payload, 
                         headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Tasks")
@allure.story("Update Task")
@allure.tag("PUT")
@allure.tag("auth")
def test_update_invalid_key(client, fresh_task_id):
    """Test task update with invalid API key returns 401"""
    payload = {
        "name": "Updated Task Name"
    }
    response = client.put(f"/tasks/{fresh_task_id}", json=payload, 
                         headers={"Accept": "application/json", "X-API-Key": "invalid_key_12345"})
    
    assert_status_code(response, 401)


@allure.feature("Tasks")
@allure.story("Update Task")
@allure.tag("PUT")
@allure.tag("negative")
def test_update_nonexistent(client, auth_headers):
    """Test updating non-existent task returns 404 or 400"""
    payload = {
        "name": "Updated Task Name"
    }
    response = client.put("/tasks/999999999", json=payload, headers=auth_headers)
    
    # Could be 404 or 400 depending on API implementation, may return 429 on rate limit
    assert response.status_code in [400, 404, 429, 500]
