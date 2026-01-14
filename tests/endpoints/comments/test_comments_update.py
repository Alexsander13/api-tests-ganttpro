"""Test for updating a comment via PUT /comments/{commentId}"""
import pytest
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Comments")
@allure.story("Update Comment")
@allure.tag("PUT")
@allure.tag("positive")
def test_update_comment_success(client, auth_headers, comment_id):
    """Test successful comment update returns 200"""
    if not comment_id:
        pytest.skip("COMMENT_ID not configured in .env")
    
    payload = {"content": "Updated comment content"}
    response = client.put(f"/comments/{comment_id}", json=payload, headers=auth_headers)
    
    assert_status_code(response, 200)
    assert_response_has_keys(response, ["status"])


@allure.feature("Comments")
@allure.story("Update Comment")
@allure.tag("PUT")
@allure.tag("auth")
def test_update_comment_unauthorized(client, comment_id):
    """Test comment update without API key returns 401"""
    if not comment_id:
        pytest.skip("COMMENT_ID not configured in .env")
    
    payload = {"content": "Updated comment content"}
    response = client.put(f"/comments/{comment_id}", json=payload, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Comments")
@allure.story("Update Comment")
@allure.tag("PUT")
@allure.tag("validation")
def test_update_comment_missing_required_field(client, auth_headers, comment_id):
    """Test comment update without required 'content' field returns 400"""
    if not comment_id:
        pytest.skip("COMMENT_ID not configured in .env")
    
    payload = {}  # Missing required 'content' field
    response = client.put(f"/comments/{comment_id}", json=payload, headers=auth_headers)
    
    assert_status_code(response, 400)
