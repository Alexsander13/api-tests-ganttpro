"""Test for deleting a link via DELETE /links/{linkId}"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Links")
@allure.story("Delete Link")
@allure.tag("DELETE")
@allure.tag("auth")
def test_delete_link_unauthorized(client, link_id):
    """Test link delete without API key returns 401"""
    if not link_id:
        pytest.skip("LINK_ID not configured in .env")
    
    response = client.delete(f"/links/{link_id}", headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Links")
@allure.story("Delete Link")
@allure.tag("DELETE")
@allure.tag("negative")
def test_delete_link_not_found(client, auth_headers):
    """Test deleting non-existent link returns 404 or 400"""
    response = client.delete("/links/999999999", headers=auth_headers)
    
    assert response.status_code in [404, 400], f"Expected 404 or 400, got {response.status_code}"


# Note: Actual deletion test is destructive and requires a disposable link ID
# TODO: Add test_delete_link_success when test data creation is implemented
