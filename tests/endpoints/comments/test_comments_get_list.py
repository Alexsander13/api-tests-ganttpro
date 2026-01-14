"""Test for getting comments list via GET /comments"""
import pytest
from src.assertions import assert_status_code, assert_response_is_list
import allure


@allure.feature("Comments")
@allure.story("Get Comments List")
@allure.tag("GET")
@allure.tag("positive")
def test_get_comments_list_success(client, auth_headers, task_id):
    """Test successful comments list retrieval returns 200"""
    params = {"taskId": [task_id]}
    response = client.get("/comments", params=params, headers=auth_headers)
    
    assert_status_code(response, 200)
    assert_response_is_list(response)


@allure.feature("Comments")
@allure.story("Get Comments List")
@allure.tag("GET")
@allure.tag("auth")
def test_get_comments_list_unauthorized(client, task_id):
    """Test comments list without API key returns 401"""
    params = {"taskId": [task_id]}
    response = client.get("/comments", params=params, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Comments")
@allure.story("Get Comments List")
@allure.tag("GET")
@allure.tag("validation")
def test_get_comments_list_missing_required_param(client, auth_headers):
    """Test comments retrieval without required taskId param returns 404"""
    response = client.get("/comments", headers=auth_headers)
    
    assert_status_code(response, 404)
