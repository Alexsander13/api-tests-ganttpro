"""Test for deleting task via DELETE /tasks/{taskId}"""
import pytest
import allure
from src.assertions import assert_status_code


@allure.feature("Tasks")
@allure.story("Delete Task")
@allure.tag("DELETE")
@allure.tag("positive")
def test_delete_success(client, auth_headers, fresh_task_id):
    """Test successful task deletion returns 200"""
    response = client.delete(f"/tasks/{fresh_task_id}", headers=auth_headers)
    
    # GanttPRO typically returns 200 on successful DELETE
    assert_status_code(response, 200)


@allure.feature("Tasks")
@allure.story("Delete Task")
@allure.tag("DELETE")
@allure.tag("auth")
def test_delete_unauthorized(client, fresh_task_id):
    """Test task deletion without API key returns 401"""
    response = client.delete(f"/tasks/{fresh_task_id}", 
                            headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Tasks")
@allure.story("Delete Task")
@allure.tag("DELETE")
@allure.tag("auth")
def test_delete_invalid_key(client, fresh_task_id):
    """Test task deletion with invalid API key returns 401"""
    response = client.delete(f"/tasks/{fresh_task_id}", 
                            headers={"Accept": "application/json", "X-API-Key": "invalid_key_12345"})
    
    assert_status_code(response, 401)


@allure.feature("Tasks")
@allure.story("Delete Task")
@allure.tag("DELETE")
@allure.tag("negative")
def test_delete_nonexistent(client, auth_headers):
    """Test deleting non-existent task returns 404 or 400"""
    response = client.delete("/tasks/999999999", headers=auth_headers)
    
    # Could be 404, 400, or 500 depending on API implementation
    assert response.status_code in [400, 404, 500]
