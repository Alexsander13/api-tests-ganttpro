"""Test for deleting a time log via DELETE /timeLogs/{timeLogId}"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Timelogs")
@allure.story("Delete Timelog")
@allure.tag("DELETE")
@allure.tag("auth")
def test_delete_time_log_unauthorized(client, timelog_id):
    """Test time log delete without API key returns 401"""
    if not timelog_id:
        pytest.skip("TIMELOG_ID not configured in .env")
    
    response = client.delete(f"/timeLogs/{timelog_id}", headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Timelogs")
@allure.story("Delete Timelog")
@allure.tag("DELETE")
@allure.tag("negative")
def test_delete_time_log_not_found(client, auth_headers):
    """Test deleting non-existent time log returns 404 or 400"""
    response = client.delete("/timeLogs/999999999", headers=auth_headers)
    
    assert response.status_code in [404, 400], f"Expected 404 or 400, got {response.status_code}"


# Note: Actual deletion test is destructive and requires a disposable timelog ID
# TODO: Add test_delete_time_log_success when test data creation is implemented
