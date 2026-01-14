"""Test for getting a link via GET /links/{linkId}"""
import pytest
from src.assertions import assert_status_code
import allure


@allure.feature("Links")
@allure.story("Get Link")
@allure.tag("GET")
@allure.tag("positive")
def test_get_link_success(client, auth_headers, link_id):
    """Test successful link retrieval returns 200"""
    if not link_id:
        pytest.skip("LINK_ID not configured in .env")
    
    response = client.get(f"/links/{link_id}", headers=auth_headers)
    
    assert_status_code(response, 200)


@allure.feature("Links")
@allure.story("Get Link")
@allure.tag("GET")
@allure.tag("auth")
def test_get_link_unauthorized(client, link_id):
    """Test link retrieval without API key returns 401"""
    if not link_id:
        pytest.skip("LINK_ID not configured in .env")
    
    response = client.get(f"/links/{link_id}", headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Links")
@allure.story("Get Link")
@allure.tag("GET")
@allure.tag("negative")
def test_get_link_not_found(client, auth_headers):
    """Test getting non-existent link returns 404 or 400"""
    response = client.get("/links/999999999", headers=auth_headers)
    
    assert response.status_code in [404, 400], f"Expected 404 or 400, got {response.status_code}"
