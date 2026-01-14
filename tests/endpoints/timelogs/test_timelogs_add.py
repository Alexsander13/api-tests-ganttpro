"""Test for adding a time log via POST /timeLogs"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Timelogs")
@allure.story("Add Timelog")
@allure.tag("POST")
@allure.tag("positive")
def test_add_time_log_to_task_success(client, auth_headers, fresh_task_id, resource_id):
    """Test successful time log creation returns 200"""
    payload = {
        "taskId": int(fresh_task_id),
        "resourceId": int(resource_id),
        "time": 60  # 60 minutes
    }
    response = client.post("/timeLogs", json=payload, headers=auth_headers)
    
    assert_status_code(response, 200)
    assert_response_has_keys(response, ["id", "taskId", "resourceId"])


@allure.feature("Timelogs")
@allure.story("Add Timelog")
@allure.tag("POST")
@allure.tag("auth")
def test_add_time_log_to_task_unauthorized(client, fresh_task_id, resource_id):
    """Test time log creation without API key returns 401"""
    payload = {
        "taskId": int(fresh_task_id),
        "resourceId": int(resource_id),
        "time": 60
    }
    response = client.post("/timeLogs", json=payload, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Timelogs")
@allure.story("Add Timelog")
@allure.tag("POST")
@allure.tag("validation")
def test_add_time_log_to_task_missing_required_fields(client, auth_headers):
    """Test time log creation without required fields returns 400"""
    payload = {}  # Missing required fields: taskId, resourceId, time
    response = client.post("/timeLogs", json=payload, headers=auth_headers)
    
    assert_status_code(response, 400)
