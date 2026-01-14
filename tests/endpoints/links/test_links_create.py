"""Test for creating a link via POST /links"""
import pytest
from src.assertions import assert_status_code
import allure


@allure.feature("Links")
@allure.story("Create Link")
@allure.tag("POST")
@allure.tag("positive")
def test_create_link_success(client, auth_headers, link_id):
    """Test successful link creation returns 200"""
    # link_id fixture automatically creates a link, so we just verify it was created
    assert link_id is not None
    assert isinstance(link_id, str)


@allure.feature("Links")
@allure.story("Create Link")
@allure.tag("POST")
@allure.tag("auth")
def test_create_link_unauthorized(client):
    """Test link creation without API key returns 401"""
    payload = {
        "source": 1,
        "target": 2,
        "type": "FS"
    }
    response = client.post("/links", json=payload, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Links")
@allure.story("Create Link")
@allure.tag("POST")
@allure.tag("validation")
def test_create_link_missing_required_fields(client, auth_headers):
    """Test link creation without required fields returns 400"""
    payload = {}  # Missing required fields: source, target, type
    response = client.post("/links", json=payload, headers=auth_headers)
    
    assert_status_code(response, 400)
