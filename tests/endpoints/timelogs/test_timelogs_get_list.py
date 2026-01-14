"""Test for getting time logs list via GET /timeLogs"""
import pytest
from src.assertions import assert_status_code, assert_response_is_list
import allure


@allure.feature("Timelogs")
@allure.story("Get Timelogs List")
@allure.tag("GET")
@allure.tag("positive")
def test_get_time_log_list_success(client, auth_headers, fresh_task_id):
    """Test successful time logs list retrieval returns 200"""
    params = {"taskId": [fresh_task_id]}
    response = client.get("/timeLogs", params=params, headers=auth_headers)
    
    assert_status_code(response, 200)
    assert_response_is_list(response)


@allure.feature("Timelogs")
@allure.story("Get Timelogs List")
@allure.tag("GET")
@allure.tag("auth")
def test_get_time_log_list_unauthorized(client, fresh_task_id):
    """Test time logs list without API key returns 401"""
    params = {"taskId": [fresh_task_id]}
    response = client.get("/timeLogs", params=params, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Timelogs")
@allure.story("Get Timelogs List")
@allure.tag("GET")
@allure.tag("validation")
def test_get_time_log_list_missing_required_param(client, auth_headers):
    """Test time log retrieval without required taskId param returns 404"""
    response = client.get("/timeLogs", headers=auth_headers)
    
    assert_status_code(response, 404)
