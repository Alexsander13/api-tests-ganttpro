"""Smoke tests for public GET endpoints and authentication.

Tests basic API availability and authentication mechanisms.
"""
import pytest
from src.assertions import assert_status_code, assert_response_is_list


@pytest.mark.smoke
def test_get_languages_success(client, auth_headers):
    """Test GET /languages returns 200 with valid auth"""
    response = client.get("/languages", headers=auth_headers)
    assert_status_code(response, 200)
    assert_response_is_list(response)


@pytest.mark.smoke
def test_get_colors_success(client, auth_headers):
    """Test GET /colors returns 200 with valid auth"""
    response = client.get("/colors", headers=auth_headers)
    assert_status_code(response, 200)
    assert_response_is_list(response)


@pytest.mark.smoke
def test_get_account_roles_success(client, auth_headers):
    """Test GET /roles/account returns 200 with valid auth"""
    response = client.get("/roles/account", headers=auth_headers)
    assert_status_code(response, 200)


@pytest.mark.smoke
def test_get_project_roles_success(client, auth_headers):
    """Test GET /roles/project returns 200 with valid auth"""
    response = client.get("/roles/project", headers=auth_headers)
    assert_status_code(response, 200)


@pytest.mark.smoke
def test_unauthorized_without_api_key(client):
    """Test requests without API key return 401"""
    response = client.get("/languages", headers={"Accept": "application/json"})
    assert_status_code(response, 401)


@pytest.mark.smoke
def test_unauthorized_with_invalid_api_key(client):
    """Test requests with invalid API key return 401"""
    headers = {
        "X-API-Key": "invalid_key_12345",
        "Accept": "application/json"
    }
    response = client.get("/languages", headers=headers)
    assert_status_code(response, 401)
