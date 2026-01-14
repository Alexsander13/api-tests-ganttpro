"""Test for getting project roles via GET /roles/project"""
import pytest
from src.assertions import assert_status_code
import allure


@allure.feature("Roles")
@allure.story("Get Project Roles")
@allure.tag("GET")
@allure.tag("positive")
def test_get_project_roles_success(client, auth_headers):
    """Test successful project roles retrieval returns 200"""
    response = client.get("/roles/project", headers=auth_headers)
    
    assert_status_code(response, 200)


@allure.feature("Roles")
@allure.story("Get Project Roles")
@allure.tag("GET")
@allure.tag("auth")
def test_get_project_roles_unauthorized(client):
    """Test project roles retrieval without API key returns 401"""
    response = client.get("/roles/project", headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)
