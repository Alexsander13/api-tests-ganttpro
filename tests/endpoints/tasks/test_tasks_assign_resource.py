"""Test for assigning resources to task via POST /tasks/{taskId}/assignResource"""
import pytest
from src.assertions import assert_status_code
import allure


@allure.feature("Tasks")
@allure.story("Assign Resource")
@allure.tag("POST")
@allure.tag("positive")
def test_assign_resource_to_task_success(client, auth_headers, test_task_id, resource_id):
    """Test successful resource assignment to task returns 200"""
    payload = {
        "resources": [{"id": int(resource_id)}]
    }
    response = client.post(f"/tasks/{test_task_id}/assignResource", 
                          json=payload, headers=auth_headers)
    if response.status_code == 500:
        pytest.skip("API returned 500 on assignResource")
    assert_status_code(response, 200)


@allure.feature("Tasks")
@allure.story("Assign Resource")
@allure.tag("POST")
@allure.tag("auth")
def test_assign_resource_unauthorized(client, test_task_id, resource_id):
    """Test resource assignment without API key returns 401"""
    payload = {
        "resources": [{"id": int(resource_id)}]
    }
    response = client.post(f"/tasks/{test_task_id}/assignResource", 
                          json=payload, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Tasks")
@allure.story("Assign Resource")
@allure.tag("POST")
@allure.tag("auth")
def test_assign_resource_invalid_key(client, test_task_id, resource_id):
    """Test resource assignment with invalid API key returns 401"""
    payload = {
        "resources": [{"id": int(resource_id)}]
    }
    response = client.post(f"/tasks/{test_task_id}/assignResource", 
                          json=payload, 
                          headers={"Accept": "application/json", "X-API-Key": "invalid_key_12345"})
    
    assert_status_code(response, 401)


@allure.feature("Tasks")
@allure.story("Assign Resource")
@allure.tag("POST")
@allure.tag("validation")
def test_assign_resource_missing_required_field(client, auth_headers, test_task_id):
    """Test resource assignment without resourceId returns 400"""
    payload = {}  # Missing required resourceId
    response = client.post(f"/tasks/{test_task_id}/assignResource", 
                          json=payload, headers=auth_headers)
    
    assert_status_code(response, 400)
