"""Test for getting colors via GET /colors"""
import pytest
from src.assertions import assert_status_code, assert_response_is_list
import allure


@allure.feature("Colors")
@allure.story("Get Colors")
@allure.tag("GET")
@allure.tag("positive")
def test_get_colors_success(client, auth_headers):
    """Test successful colors retrieval returns 200"""
    response = client.get("/colors", headers=auth_headers)
    
    assert_status_code(response, 200)
    assert_response_is_list(response)


@allure.feature("Colors")
@allure.story("Get Colors")
@allure.tag("GET")
@allure.tag("auth")
def test_get_colors_unauthorized(client):
    """Test colors retrieval without API key returns 401"""
    response = client.get("/colors", headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)
