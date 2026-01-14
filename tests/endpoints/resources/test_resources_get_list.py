"""Test for getting resources list via GET /resources"""
import pytest
from src.assertions import assert_status_code, assert_response_is_list
import allure


@allure.feature("Resources")
@allure.story("Get Resources List")
@allure.tag("GET")
@allure.tag("positive")
def test_get_resources_list_success(client, auth_headers):
    """Test successful resources list retrieval returns 200"""
    response = client.get("/resources", headers=auth_headers)
    
    assert_status_code(response, 200)
    assert_response_is_list(response)


@allure.feature("Resources")
@allure.story("Get Resources List")
@allure.tag("GET")
@allure.tag("auth")
def test_get_resources_list_unauthorized(client):
    """Test resources list without API key returns 401"""
    response = client.get("/resources", headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)
