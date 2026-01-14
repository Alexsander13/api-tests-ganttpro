"""Test for getting projects list via GET /projects"""
import pytest
from src.assertions import assert_status_code
import allure


@allure.feature("Projects")
@allure.story("Get Projects List")
@allure.tag("GET")
@allure.tag("positive")
def test_get_projects_list_success(client, auth_headers):
    """Test successful projects list retrieval returns 200"""
    response = client.get("/projects", headers=auth_headers)
    
    assert_status_code(response, 200)
    # Response should be a list
    assert isinstance(response.json(), list), "Response should be a list of projects"


@allure.feature("Projects")
@allure.story("Get Projects List")
@allure.tag("GET")
@allure.tag("auth")
def test_get_projects_list_unauthorized(client):
    """Test projects list retrieval without API key returns 401"""
    response = client.get("/projects", headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Projects")
@allure.story("Get Projects List")
@allure.tag("GET")
@allure.tag("auth")
def test_get_projects_list_invalid_key(client):
    """Test projects list retrieval with invalid API key returns 401"""
    response = client.get("/projects", headers={"Accept": "application/json", "X-API-Key": "invalid_key_12345"})
    
    assert_status_code(response, 401)
