"""Test for deleting a task via DELETE /tasks/{taskId}"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Tasks")
@allure.story("Delete Task")
@allure.tag("DELETE")
@allure.tag("auth")
def test_delete_task_unauthorized(client, task_id):
    """Test task delete without API key returns 401"""

    response = client.delete(f"/tasks/{task_id}", headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Tasks")
@allure.story("Delete Task")
@allure.tag("DELETE")
@allure.tag("negative")
def test_delete_task_not_found(client, auth_headers):
    """Test deleting non-existent task returns 404"""
    # Use a very large ID unlikely to exist
    response = client.delete("/tasks/999999999", headers=auth_headers)
    
    # Should return 404 for not found
    assert response.status_code in [404, 400], f"Expected 404 or 400, got {response.status_code}"


# Note: Actual deletion test is destructive and requires a disposable task ID
# TODO: Add test_delete_task_success when test data creation is implemented
