"""Test for getting a time log via GET /timeLogs/{timeLogId}"""
import pytest
from src.assertions import assert_status_code
import allure


@allure.feature("Timelogs")
@allure.story("Get Timelog")
@allure.tag("GET")
@allure.tag("positive")
def test_get_time_log_success(client, auth_headers, timelog_id):
    """Test successful time log retrieval returns 200"""
    if not timelog_id:
        pytest.skip("TIMELOG_ID not configured in .env")
    
    response = client.get(f"/timeLogs/{timelog_id}", headers=auth_headers)
    
    assert_status_code(response, 200)


@allure.feature("Timelogs")
@allure.story("Get Timelog")
@allure.tag("GET")
@allure.tag("auth")
def test_get_time_log_unauthorized(client, timelog_id):
    """Test time log retrieval without API key returns 401"""
    if not timelog_id:
        pytest.skip("TIMELOG_ID not configured in .env")
    
    response = client.get(f"/timeLogs/{timelog_id}", headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Timelogs")
@allure.story("Get Timelog")
@allure.tag("GET")
@allure.tag("negative")
def test_get_time_log_not_found(client, auth_headers):
    """Test getting non-existent time log returns 404 or 400"""
    response = client.get("/timeLogs/999999999", headers=auth_headers)
    
    assert response.status_code in [404, 400], f"Expected 404 or 400, got {response.status_code}"
