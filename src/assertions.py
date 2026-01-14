"""Reusable assertion helpers for API tests.

Provides common assertions for status codes, response structure,
and schema validation.
"""
from typing import Any, Dict, List, Optional, Union
from requests import Response
import json


def assert_status_code(response: Response, expected_status: int, message: Optional[str] = None) -> None:
    """Assert response has expected status code.
    
    Args:
        response: HTTP response object.
        expected_status: Expected status code.
        message: Optional custom error message.
    
    Raises:
        AssertionError: If status code doesn't match.
    """
    if message is None:
        message = (
            f"Expected status {expected_status}, got {response.status_code}. "
            f"URL: {response.url}, Response: {response.text[:200]}"
        )
    
    assert response.status_code == expected_status, message


def assert_response_has_keys(response: Response, keys: List[str]) -> None:
    """Assert response JSON contains specific keys.
    
    Args:
        response: HTTP response object.
        keys: List of keys that should be present.
    
    Raises:
        AssertionError: If any key is missing.
    """
    try:
        data = response.json()
    except json.JSONDecodeError:
        raise AssertionError(f"Response is not valid JSON: {response.text[:200]}")
    
    if not isinstance(data, dict):
        raise AssertionError(f"Response is not a JSON object: {type(data)}")
    
    missing_keys = [key for key in keys if key not in data]
    assert not missing_keys, f"Missing keys in response: {missing_keys}. Response: {data}"


def assert_response_is_list(response: Response, min_length: Optional[int] = None) -> None:
    """Assert response is a JSON list.
    
    Args:
        response: HTTP response object.
        min_length: Minimum expected list length (optional).
    
    Raises:
        AssertionError: If response is not a list or length requirement not met.
    """
    try:
        data = response.json()
    except json.JSONDecodeError:
        raise AssertionError(f"Response is not valid JSON: {response.text[:200]}")
    
    assert isinstance(data, list), f"Response is not a list: {type(data)}"
    
    if min_length is not None:
        assert len(data) >= min_length, f"Expected at least {min_length} items, got {len(data)}"


def assert_response_contains_text(response: Response, text: str) -> None:
    """Assert response text contains specific string.
    
    Args:
        response: HTTP response object.
        text: Text that should be present in response.
    
    Raises:
        AssertionError: If text not found.
    """
    assert text in response.text, f"Text '{text}' not found in response: {response.text[:200]}"


def assert_json_structure(data: Any, expected_keys: List[str], path: str = "root") -> None:
    """Assert JSON object has expected structure.
    
    Args:
        data: JSON data to validate.
        expected_keys: List of keys that should be present.
        path: Path in JSON structure (for error messages).
    
    Raises:
        AssertionError: If structure doesn't match.
    """
    if not isinstance(data, dict):
        raise AssertionError(f"Expected object at {path}, got {type(data)}")
    
    missing_keys = [key for key in expected_keys if key not in data]
    assert not missing_keys, f"Missing keys at {path}: {missing_keys}"


def assert_error_response(response: Response, expected_status: int) -> None:
    """Assert response is an error with expected status.
    
    Args:
        response: HTTP response object.
        expected_status: Expected error status code.
    
    Raises:
        AssertionError: If response is not an error or status doesn't match.
    """
    assert_status_code(response, expected_status)
    
    # Error responses should contain some content
    assert len(response.text) > 0, "Error response should not be empty"
