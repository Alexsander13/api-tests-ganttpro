"""Test for getting comments by project ID via GET /comments/getByProjectId"""
import pytest
from src.assertions import assert_status_code
import allure


@allure.feature("Comments")
@allure.story("Get Comments by Project")
@allure.tag("GET")
@allure.tag("positive")
def test_get_comments_by_project_id_success(client, auth_headers, project_id):
    """Test successful comments retrieval by project ID returns 200"""
    if not project_id:
        pytest.skip("PROJECT_ID not configured in .env")
    
    params = {"projectId": project_id}
    response = client.get("/comments/getByProjectId", params=params, headers=auth_headers)
    
    assert_status_code(response, 200)


@allure.feature("Comments")
@allure.story("Get Comments by Project")
@allure.tag("GET")
@allure.tag("auth")
def test_get_comments_by_project_id_unauthorized(client, project_id):
    """Test comments retrieval without API key returns 401"""
    if not project_id:
        pytest.skip("PROJECT_ID not configured in .env")
    
    params = {"projectId": project_id}
    response = client.get("/comments/getByProjectId", params=params, headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Comments")
@allure.story("Get Comments by Project")
@allure.tag("GET")
@allure.tag("validation")
def test_get_comments_by_project_id_missing_required_param(client, auth_headers):
    """Test comments retrieval without required projectId param returns 404"""
    response = client.get("/comments/getByProjectId", headers=auth_headers)
    
    assert_status_code(response, 404)
