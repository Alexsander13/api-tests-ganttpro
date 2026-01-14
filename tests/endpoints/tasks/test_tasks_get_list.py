"""Test for getting tasks list via GET /tasks"""
import pytest
import allure
from src.assertions import assert_status_code


@allure.feature("Tasks")
@allure.story("Get Tasks List")
@allure.tag("GET")
@allure.tag("positive")
def test_get_list_success(client, auth_headers, project_id):
    """Test successful tasks list retrieval by projectId returns 200"""
    response = client.get("/tasks", params={"projectId": int(project_id)}, headers=auth_headers)
    
    assert_status_code(response, 200)
    # Response should be a list
    assert isinstance(response.json(), list), "Response should be a list of tasks"


@allure.feature("Tasks")
@allure.story("Get Tasks List")
@allure.tag("GET")
@allure.tag("auth")
def test_get_list_unauthorized(client, project_id):
    """Test tasks list retrieval without API key returns 401"""
    response = client.get("/tasks", params={"projectId": int(project_id)}, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Tasks")
@allure.story("Get Tasks List")
@allure.tag("GET")
@allure.tag("auth")
def test_get_list_invalid_key(client, project_id):
    """Test tasks list retrieval with invalid API key returns 401"""
    response = client.get("/tasks", params={"projectId": int(project_id)}, 
                         headers={"Accept": "application/json", "X-API-Key": "invalid_key_12345"})
    
    assert_status_code(response, 401)


@allure.feature("Tasks")
@allure.story("Get Tasks List")
@allure.tag("GET")
@allure.tag("validation")
def test_get_list_missing_project_id(client, auth_headers):
    """Test tasks list retrieval without required projectId param returns 404"""
    response = client.get("/tasks", headers=auth_headers)
    
    # API returns 404 when projectId is missing
    assert_status_code(response, 404)
