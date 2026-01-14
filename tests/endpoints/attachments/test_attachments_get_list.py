"""Test for getting attachments list via GET /attachments"""
import pytest
from src.assertions import assert_status_code
import allure


@allure.feature("Attachments")
@allure.story("Get Attachments List")
@allure.tag("GET")
@allure.tag("positive")
def test_get_attachments_list_success(client, auth_headers, task_id):
    """Test successful attachments list retrieval returns 200"""
    params = {"taskId": [task_id]}
    response = client.get("/attachments", params=params, headers=auth_headers)
    
    assert_status_code(response, 200)


@allure.feature("Attachments")
@allure.story("Get Attachments List")
@allure.tag("GET")
@allure.tag("auth")
def test_get_attachments_list_unauthorized(client, task_id):
    """Test attachments list without API key returns 401"""
    params = {"taskId": [task_id]}
    response = client.get("/attachments", params=params, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Attachments")
@allure.story("Get Attachments List")
@allure.tag("GET")
@allure.tag("validation")
def test_get_attachments_list_missing_required_param(client, auth_headers):
    """Test attachments retrieval without required taskId param returns 404"""
    response = client.get("/attachments", headers=auth_headers)
    
    assert_status_code(response, 404)
