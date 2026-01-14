"""Test for getting resources list via GET /resources"""
from src.assertions import assert_status_code, assert_response_has_keys
import allure


@allure.feature("Resources")
@allure.story("Get Resources")
@allure.tag("GET")
@allure.tag("positive")
def test_get_resources_list_success(client, auth_headers):
    """Test successful resources list retrieval returns 200"""
    response = client.get("/resources", headers=auth_headers)
    
    assert_status_code(response, 200)
    data = response.json()
    # Expecting a list or list response
    assert isinstance(data, list) or "items" in data or "data" in data, \
        "Response should contain a list or have 'items'/'data' key"


@allure.feature("Resources")
@allure.story("Get Resources")
@allure.tag("GET")
@allure.tag("auth")
def test_get_resources_list_unauthorized(client):
    """Test resources list retrieval without API key returns 401"""
    response = client.get("/resources", headers={"Accept": "application/json"})
    
    assert_status_code(response, 401)


@allure.feature("Resources")
@allure.story("Get Resources")
@allure.tag("GET")
@allure.tag("auth")
def test_get_resources_list_invalid_key(client):
    """Test resources list retrieval with invalid API key returns 401"""
    response = client.get("/resources", 
                         headers={"Accept": "application/json", "X-API-Key": "invalid_key_12345"})
    
    assert_status_code(response, 401)
