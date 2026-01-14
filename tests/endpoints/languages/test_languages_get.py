"""Test for getting languages via GET /languages"""
import pytest
from src.assertions import assert_status_code, assert_response_is_list
import allure


@allure.feature("Languages")
@allure.story("Get Languages")
@allure.tag("GET")
@allure.tag("positive")
def test_get_languages_success(client, auth_headers):
    """Test successful languages retrieval returns 200"""
    response = client.get("/languages", headers=auth_headers)
    
    assert_status_code(response, 200)
    assert_response_is_list(response)


@allure.feature("Languages")
@allure.story("Get Languages")
@allure.tag("GET")
@allure.tag("auth")
def test_get_languages_unauthorized(client):
    """Test languages retrieval without API key returns 401"""
    response = client.get("/languages", headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)
