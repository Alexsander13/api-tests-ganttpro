"""Test for updating a link via PUT /links/{linkId}"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Links")
@allure.story("Update Link")
@allure.tag("PUT")
@allure.tag("positive")
def test_update_link_success(client, auth_headers, link_id):
    """Test successful link update returns 200"""
    if not link_id:
        pytest.skip("LINK_ID not configured in .env")
    
    payload = {"type": 0}  # Type must be numeric: 0=FS, 1=SS, 2=FF, 3=SF
    response = client.put(f"/links/{link_id}", json=payload, headers=auth_headers)
    
    assert_status_code(response, 200)
    assert_response_has_keys(response, ["status"])


@allure.feature("Links")
@allure.story("Update Link")
@allure.tag("PUT")
@allure.tag("auth")
def test_update_link_unauthorized(client, link_id):
    """Test link update without API key returns 401"""
    if not link_id:
        pytest.skip("LINK_ID not configured in .env")
    
    payload = {"type": "FS"}
    response = client.put(f"/links/{link_id}", json=payload, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Links")
@allure.story("Update Link")
@allure.tag("PUT")
@allure.tag("validation")
def test_update_link_invalid_id(client, auth_headers):
    """Test link update with invalid ID returns 400 or 404"""
    payload = {"type": "FS"}
    response = client.put("/links/-1", json=payload, headers=auth_headers)
    
    assert response.status_code in [400, 404], f"Expected 400 or 404, got {response.status_code}"
