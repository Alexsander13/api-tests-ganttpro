"""Test for deleting attachment via DELETE /attachments/{attachmentId}"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Attachments")
@allure.story("Delete Attachment")
@allure.tag("DELETE")
@allure.tag("auth")
def test_delete_attachment_unauthorized(client, attachment_id):
    """Test attachment delete without API key returns 401"""
    if not attachment_id:
        pytest.skip("ATTACHMENT_ID not configured in .env")
    
    response = client.delete(f"/attachments/{attachment_id}", headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Attachments")
@allure.story("Delete Attachment")
@allure.tag("DELETE")
@allure.tag("negative")
def test_delete_attachment_not_found(client, auth_headers):
    """Test deleting non-existent attachment returns 404 or 400"""
    response = client.delete("/attachments/999999999", headers=auth_headers)
    
    assert response.status_code in [404, 400], f"Expected 404 or 400, got {response.status_code}"


# Note: Actual deletion test is destructive and requires a disposable attachment ID
# TODO: Add test_delete_attachment_success when test data creation is implemented
