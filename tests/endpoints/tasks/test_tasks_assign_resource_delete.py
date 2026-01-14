"""Test for deleting resource assignment via DELETE /tasks/{taskId}/assignResource"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Tasks")
@allure.story("Delete Assignment")
@allure.tag("DELETE")
@allure.tag("positive")
def test_delete_assign_from_task_success(client, auth_headers, task_id, resource_id):
    """Test successful resource unassignment returns 200"""
    params = {"resourceId": [resource_id]}
    response = client.delete(f"/tasks/{task_id}/assignResource", params=params, headers=auth_headers)
    
    assert_status_code(response, 200)
    assert_response_has_keys(response, ["status"])


@allure.feature("Tasks")
@allure.story("Delete Assignment")
@allure.tag("DELETE")
@allure.tag("auth")
def test_delete_assign_from_task_unauthorized(client, task_id):
    """Test resource unassignment without API key returns 401"""
    params = {"resourceId": [1]}
    response = client.delete(f"/tasks/{task_id}/assignResource", params=params, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Tasks")
@allure.story("Delete Assignment")
@allure.tag("DELETE")
@allure.tag("validation")
def test_delete_assign_from_task_missing_required_param(client, auth_headers, task_id):
    """Test resource unassignment without required resourceId param returns 404"""
    # Missing required resourceId query param
    response = client.delete(f"/tasks/{task_id}/assignResource", headers=auth_headers)
    
    assert_status_code(response, 404)
