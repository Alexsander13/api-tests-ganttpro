"""Test for getting attachments by project ID via GET /attachments/getByProjectId"""
import pytest
from src.assertions import assert_status_code
import allure


@allure.feature("Attachments")
@allure.story("Get Attachments by Project")
@allure.tag("GET")
@allure.tag("positive")
def test_get_attachments_by_project_id_success(client, auth_headers, project_id):
    """Test successful attachments retrieval by project ID returns 200"""
    if not project_id:
        pytest.skip("PROJECT_ID not configured in .env")
    
    params = {"projectId": project_id}
    response = client.get("/attachments/getByProjectId", params=params, headers=auth_headers)
    
    assert_status_code(response, 200)


@allure.feature("Attachments")
@allure.story("Get Attachments by Project")
@allure.tag("GET")
@allure.tag("auth")
def test_get_attachments_by_project_id_unauthorized(client, project_id):
    """Test attachments retrieval without API key returns 401"""
    if not project_id:
        pytest.skip("PROJECT_ID not configured in .env")
    
    params = {"projectId": project_id}
    response = client.get("/attachments/getByProjectId", params=params, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Attachments")
@allure.story("Get Attachments by Project")
@allure.tag("GET")
@allure.tag("validation")
def test_get_attachments_by_project_id_missing_required_param(client, auth_headers):
    """Test attachments retrieval without required projectId param returns 404"""
    response = client.get("/attachments/getByProjectId", headers=auth_headers)
    
    assert_status_code(response, 404)
