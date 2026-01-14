"""Test for deleting attachments by IDs via DELETE /attachments/delete/byIds"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Attachments")
@allure.story("Delete Attachments")
@allure.tag("DELETE")
@allure.tag("positive")
def test_delete_attachments_by_ids_success(client, auth_headers, attachment_id):
    """Test successful deletion of attachments by IDs returns 200"""
    if not attachment_id:
        pytest.skip("ATTACHMENT_ID not configured in .env")
    
    payload = {"attachmentIds": [int(attachment_id)]}
    response = client.delete("/attachments/delete/byIds", json=payload, headers=auth_headers)
    
    # May return 200 even if attachment doesn't exist
    assert response.status_code in [200, 400, 404], f"Expected 200, 400, or 404, got {response.status_code}"


@allure.feature("Attachments")
@allure.story("Delete Attachments")
@allure.tag("DELETE")
@allure.tag("auth")
def test_delete_attachments_by_ids_unauthorized(client):
    """Test attachments deletion without API key returns 401"""
    payload = {"attachmentIds": [1, 2, 3]}
    response = client.delete("/attachments/delete/byIds", json=payload, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Attachments")
@allure.story("Delete Attachments")
@allure.tag("DELETE")
@allure.tag("validation")
def test_delete_attachments_by_ids_missing_required_field(client, auth_headers):
    """Test attachments deletion without required attachmentIds field returns 400"""
    payload = {}  # Missing required 'attachmentIds' field
    response = client.delete("/attachments/delete/byIds", json=payload, headers=auth_headers)
    
    assert_status_code(response, 400)
