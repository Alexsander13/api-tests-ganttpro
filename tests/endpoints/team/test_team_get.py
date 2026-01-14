"""Test for getting team info via GET /team"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Team")
@allure.story("Get Team")
@allure.tag("GET")
@allure.tag("positive")
def test_get_team_success(client, auth_headers):
    """Test successful team info retrieval returns 200"""
    response = client.get("/team", headers=auth_headers)
    
    assert_status_code(response, 200)
    assert_response_has_keys(response, ["id", "name"])


@allure.feature("Team")
@allure.story("Get Team")
@allure.tag("GET")
@allure.tag("auth")
def test_get_team_unauthorized(client):
    """Test team info retrieval without API key returns 401"""
    response = client.get("/team", headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Team")
@allure.story("Get Team")
@allure.tag("GET")
@allure.tag("auth")
def test_get_team_invalid_key(client):
    """Test team info retrieval with invalid API key returns 401"""
    response = client.get("/team", headers={"Accept": "application/json", "X-API-Key": "invalid_key_12345"})
    
    assert_status_code(response, 401)
