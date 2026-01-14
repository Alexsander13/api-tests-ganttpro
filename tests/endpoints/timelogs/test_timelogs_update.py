"""Test for updating a time log via PUT /timeLogs/{timeLogId}"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Timelogs")
@allure.story("Update Timelog")
@allure.tag("PUT")
@allure.tag("positive")
def test_update_time_log_success(client, auth_headers, timelog_id):
    """Test successful time log update returns 200"""
    if not timelog_id:
        pytest.skip("TIMELOG_ID not configured in .env")
    
    payload = {"time": 120}  # Update time to 120 minutes
    response = client.put(f"/timeLogs/{timelog_id}", json=payload, headers=auth_headers)
    
    assert_status_code(response, 200)
    assert_response_has_keys(response, ["status"])


@allure.feature("Timelogs")
@allure.story("Update Timelog")
@allure.tag("PUT")
@allure.tag("auth")
def test_update_time_log_unauthorized(client, timelog_id):
    """Test time log update without API key returns 401"""
    if not timelog_id:
        pytest.skip("TIMELOG_ID not configured in .env")
    
    payload = {"time": 120}
    response = client.put(f"/timeLogs/{timelog_id}", json=payload, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Timelogs")
@allure.story("Update Timelog")
@allure.tag("PUT")
@allure.tag("validation")
def test_update_time_log_invalid_id(client, auth_headers):
    """Test time log update with invalid ID returns 400 or 404"""
    payload = {"time": 120}
    response = client.put("/timeLogs/-1", json=payload, headers=auth_headers)
    
    assert response.status_code in [400, 404], f"Expected 400 or 404, got {response.status_code}"
