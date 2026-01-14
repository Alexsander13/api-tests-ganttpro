"""Test for getting account roles via GET /roles/account"""
import pytest
from src.assertions import assert_status_code
import allure


@allure.feature("Roles")
@allure.story("Get Account Roles")
@allure.tag("GET")
@allure.tag("positive")
def test_get_account_roles_success(client, auth_headers):
    """Test successful account roles retrieval returns 200"""
    response = client.get("/roles/account", headers=auth_headers)
    
    assert_status_code(response, 200)


@allure.feature("Roles")
@allure.story("Get Account Roles")
@allure.tag("GET")
@allure.tag("auth")
def test_get_account_roles_unauthorized(client):
    """Test account roles retrieval without API key returns 401"""
    response = client.get("/roles/account", headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)
