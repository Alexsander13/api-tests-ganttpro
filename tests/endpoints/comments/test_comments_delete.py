"""Test for deleting a comment via DELETE /comments/{commentId}"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Comments")
@allure.story("Delete Comment")
@allure.tag("DELETE")
@allure.tag("auth")
def test_delete_comment_unauthorized(client, comment_id):
    """Test comment delete without API key returns 401"""
    if not comment_id:
        pytest.skip("COMMENT_ID not configured in .env")
    
    response = client.delete(f"/comments/{comment_id}", headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Comments")
@allure.story("Delete Comment")
@allure.tag("DELETE")
@allure.tag("negative")
def test_delete_comment_not_found(client, auth_headers):
    """Test deleting non-existent comment returns 404 or 400"""
    response = client.delete("/comments/999999999", headers=auth_headers)
    
    assert response.status_code in [404, 400], f"Expected 404 or 400, got {response.status_code}"


# Note: Actual deletion test is destructive and requires a disposable comment ID
# TODO: Add test_delete_comment_success when test data creation is implemented
