"""Test for adding a comment via POST /comments"""
import pytest
from src.assertions import assert_status_code
import allure


@allure.feature("Comments")
@allure.story("Add Comment")
@allure.tag("POST")
@allure.tag("positive")
def test_add_comment_to_task_success(client, auth_headers, task_id, user_id):
    """Test successful comment creation returns 200"""
    payload = {
        "taskId": int(task_id),
        "userId": int(user_id),
        "content": "Test comment content"
    }
    response = client.post("/comments", json=payload, headers=auth_headers)
    
    assert_status_code(response, 200)


@allure.feature("Comments")
@allure.story("Add Comment")
@allure.tag("POST")
@allure.tag("auth")
def test_add_comment_to_task_unauthorized(client, task_id, user_id):
    """Test comment creation without API key returns 401"""
    payload = {
        "taskId": int(task_id),
        "userId": int(user_id),
        "content": "Test comment content"
    }
    response = client.post("/comments", json=payload, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Comments")
@allure.story("Add Comment")
@allure.tag("POST")
@allure.tag("validation")
def test_add_comment_to_task_missing_required_fields(client, auth_headers):
    """Test comment creation without required fields returns 400"""
    payload = {}  # Missing required fields: taskId, userId, content
    response = client.post("/comments", json=payload, headers=auth_headers)
    
    assert_status_code(response, 400)
