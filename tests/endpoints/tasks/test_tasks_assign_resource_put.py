"""Test for updating task resources via PUT /tasks/{taskId}/assignResource"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Tasks")
@allure.story("Update Resource")
@allure.tag("PUT")
@allure.tag("positive")
def test_update_task_resource_success(client, auth_headers, task_id, resource_id):
    """Test successful task resource update returns 200"""
    payload = {
        "resources": [
            {"resourceId": int(resource_id), "resourceValue": 100}
        ]
    }
    response = client.put(f"/tasks/{task_id}/assignResource", json=payload, headers=auth_headers)
    
    assert_status_code(response, 200)
    assert_response_has_keys(response, ["status"])


@allure.feature("Tasks")
@allure.story("Update Resource")
@allure.tag("PUT")
@allure.tag("auth")
def test_update_task_resource_unauthorized(client, task_id):
    """Test task resource update without API key returns 401"""
    payload = {"resources": [{"resourceId": 1, "resourceValue": 100}]}
    response = client.put(f"/tasks/{task_id}/assignResource", json=payload, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Tasks")
@allure.story("Update Resource")
@allure.tag("PUT")
@allure.tag("validation")
def test_update_task_resource_missing_required_field(client, auth_headers, task_id):
    """Test task resource update without required 'resources' field returns 400"""
    payload = {}  # Missing required 'resources' field
    response = client.put(f"/tasks/{task_id}/assignResource", json=payload, headers=auth_headers)
    
    assert_status_code(response, 400)
