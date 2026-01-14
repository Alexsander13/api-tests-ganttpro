"""HTTP client wrapper for GanttPRO API.

Provides a thin wrapper over requests library with base URL,
authentication, and logging capabilities.
"""
import logging
import json
from typing import Any, Dict, Optional, List
import requests
from requests import Response

from .config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HTTPClient:
    """HTTP client for API requests."""
    
    def __init__(self, base_url: Optional[str] = None):
        """Initialize HTTP client.
        
        Args:
            base_url: Base URL for API requests. Defaults to Config.BASE_URL.
        """
        self.base_url = base_url or Config.BASE_URL
        self.session = requests.Session()
        self.request_history: List[Dict[str, Any]] = []
        self.last_response: Optional[Response] = None  # Для Allure отчётов
    
    def _build_url(self, path: str) -> str:
        """Build full URL from path.
        
        Args:
            path: API endpoint path (e.g., '/tasks/123').
        
        Returns:
            Full URL.
        """
        # Remove leading slash from path if present to avoid double slashes
        path = path.lstrip('/')
        return f"{self.base_url}/{path}"
    
    def _log_request(self, method: str, url: str, **kwargs) -> None:
        """Log request details.
        
        Args:
            method: HTTP method.
            url: Request URL.
            **kwargs: Additional request parameters.
        """
        logger.info(f"{method.upper()} {url}")
        if kwargs.get('json'):
            logger.debug(f"Request body: {kwargs['json']}")
        if kwargs.get('params'):
            logger.debug(f"Query params: {kwargs['params']}")
    
    def _log_response(self, response: Response) -> None:
        """Log response details.
        
        Args:
            response: HTTP response object.
        """
        logger.info(f"Response status: {response.status_code}")
        
        # Store in history
        if self.request_history:
            self.request_history[-1]['response'] = {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'body': response.text[:500] if response.text else None
            }
        
        if response.status_code >= 400:
            logger.error(f"Response body: {response.text}")
        else:
            logger.debug(f"Response body: {response.text[:200]}")
    
    def request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Response:
        """Make HTTP request.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            path: API endpoint path.
            headers: Request headers.
            **kwargs: Additional arguments passed to requests.
        
        Returns:
            Response object.
        """
        url = self._build_url(path)
        
        # Merge headers
        merged_headers = {"Accept": "application/json"}
        if headers:
            merged_headers.update(headers)
        
        # Store request details
        request_info = {
            'method': method,
            'url': url,
            'headers': {k: v for k, v in merged_headers.items() if k != 'X-API-Key'},  # Don't log API key
            'params': kwargs.get('params'),
            'body': kwargs.get('json') or kwargs.get('data'),
            'response': None
        }
        self.request_history.append(request_info)
        
        self._log_request(method, url, **kwargs)
        
        response = self.session.request(
            method=method,
            url=url,
            headers=merged_headers,
            **kwargs
        )
        
        self.last_response = response  # Сохраняем для Allure
        self._log_response(response)
        return response
    
    def get_last_request(self) -> Optional[Dict[str, Any]]:
        """Get details of the last request made.
        
        Returns:
            Dictionary with request/response details or None.
        """
        return self.request_history[-1] if self.request_history else None
    
    def clear_history(self) -> None:
        """Clear request history."""
        self.request_history = []
    
    def get(self, path: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Response:
        """Make GET request.
        
        Args:
            path: API endpoint path.
            headers: Request headers.
            **kwargs: Additional arguments.
        
        Returns:
            Response object.
        """
        return self.request("GET", path, headers=headers, **kwargs)
    
    def post(self, path: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Response:
        """Make POST request.
        
        Args:
            path: API endpoint path.
            headers: Request headers.
            **kwargs: Additional arguments.
        
        Returns:
            Response object.
        """
        return self.request("POST", path, headers=headers, **kwargs)
    
    def put(self, path: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Response:
        """Make PUT request.
        
        Args:
            path: API endpoint path.
            headers: Request headers.
            **kwargs: Additional arguments.
        
        Returns:
            Response object.
        """
        return self.request("PUT", path, headers=headers, **kwargs)
    
    def delete(self, path: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Response:
        """Make DELETE request.
        
        Args:
            path: API endpoint path.
            headers: Request headers.
            **kwargs: Additional arguments.
        
        Returns:
            Response object.
        """
        return self.request("DELETE", path, headers=headers, **kwargs)
