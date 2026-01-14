"""Test for assigning resources to task via POST /tasks/{taskId}/assignResource"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Tasks")
@allure.story("Assign Resources")
@allure.tag("POST")
@allure.tag("positive")
def test_assign_resources_to_task_success(client, auth_headers, task_id, resource_id):
    """Test successful resource assignment returns 200"""
    payload = {
        "resources": [
            {"resourceId": int(resource_id), "resourceValue": 100}
        ]
    }
    response = client.post(f"/tasks/{task_id}/assignResource", json=payload, headers=auth_headers)
    
    assert_status_code(response, 200)
    assert_response_has_keys(response, ["status"])


@allure.feature("Tasks")
@allure.story("Assign Resources")
@allure.tag("POST")
@allure.tag("auth")
def test_assign_resources_to_task_unauthorized(client, task_id):
    """Test resource assignment without API key returns 401"""
    payload = {"resources": [{"resourceId": 1, "resourceValue": 100}]}
    response = client.post(f"/tasks/{task_id}/assignResource", json=payload, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Tasks")
@allure.story("Assign Resources")
@allure.tag("POST")
@allure.tag("validation")
def test_assign_resources_to_task_missing_required_field(client, auth_headers, task_id):
    """Test resource assignment without required 'resources' field returns 400"""
    payload = {}  # Missing required 'resources' field
    response = client.post(f"/tasks/{task_id}/assignResource", json=payload, headers=auth_headers)
    
    assert_status_code(response, 400)
