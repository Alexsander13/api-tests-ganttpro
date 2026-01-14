"""Test for adding attachment via POST /attachments"""
import pytest
import tempfile
import os
import allure
from src.assertions import assert_status_code


@allure.feature("Attachments")
@allure.story("Add Attachment")
@allure.tag("POST")
@allure.tag("positive")
def test_add_success(client, auth_headers, task_id, user_id):
    """Test successful attachment upload returns 200"""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_file:
        tmp_file.write("Test attachment content")
        tmp_file_path = tmp_file.name
    
    try:
        with open(tmp_file_path, 'rb') as f:
            files = {'file': ('test_file.txt', f, 'text/plain')}
            data = {
                'taskId': task_id,
                'userId': user_id
            }
            # Note: For multipart/form-data, do not set Content-Type header manually
            response = client.post("/attachments", files=files, data=data, headers=auth_headers)
        
        assert_status_code(response, 200)
    finally:
        # Clean up temporary file
        os.unlink(tmp_file_path)


@allure.feature("Attachments")
@allure.story("Add Attachment")
@allure.tag("POST")
@allure.tag("auth")
def test_add_unauthorized(client, task_id, user_id):
    """Test attachment upload without API key returns 401"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_file:
        tmp_file.write("Test attachment content")
        tmp_file_path = tmp_file.name
    
    try:
        with open(tmp_file_path, 'rb') as f:
            files = {'file': ('test_file.txt', f, 'text/plain')}
            data = {
                'taskId': task_id,
                'userId': user_id
            }
            response = client.post("/attachments", files=files, data=data, headers={"Accept": "application/json"})
        
        assert_status_code(response, 401)
    finally:
        os.unlink(tmp_file_path)


@allure.feature("Attachments")
@allure.story("Add Attachment")
@allure.tag("POST")
@allure.tag("validation")
def test_add_missing_fields(client, auth_headers):
    """Test attachment upload without required fields returns 400"""
    # Missing required fields
    response = client.post("/attachments", json={}, headers=auth_headers)
    
    assert_status_code(response, 400)
