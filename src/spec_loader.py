"""API specification loader.

Loads api_spec.json and provides helper methods to query endpoint information.
"""
import json
import os
from typing import Any, Dict, List, Optional


class SpecLoader:
    """Loader for API specification."""
    
    def __init__(self, spec_path: Optional[str] = None):
        """Initialize spec loader.
        
        Args:
            spec_path: Path to api_spec.json. Defaults to project root.
        """
        if spec_path is None:
            # Default to api_spec.json in project root
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            spec_path = os.path.join(project_root, "api_spec.json")
        
        self.spec_path = spec_path
        self.spec = self._load_spec()
    
    def _load_spec(self) -> Dict[str, Any]:
        """Load API specification from JSON file.
        
        Returns:
            Parsed API specification.
        
        Raises:
            FileNotFoundError: If spec file not found.
            json.JSONDecodeError: If spec file is invalid JSON.
        """
        with open(self.spec_path, 'r') as f:
            return json.load(f)
    
    def get_base_url(self) -> str:
        """Get API base URL from spec.
        
        Returns:
            Base URL string.
        """
        return self.spec.get("api", {}).get("baseUrl", "")
    
    def get_endpoints(self) -> List[Dict[str, Any]]:
        """Get all endpoints from spec.
        
        Returns:
            List of endpoint definitions.
        """
        return self.spec.get("endpoints", [])
    
    def get_endpoint_by_operation_id(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """Get endpoint by operation ID.
        
        Args:
            operation_id: Operation ID to search for.
        
        Returns:
            Endpoint definition or None if not found.
        """
        for endpoint in self.get_endpoints():
            if endpoint.get("operationId") == operation_id:
                return endpoint
        return None
    
    def get_endpoints_by_path_prefix(self, prefix: str) -> List[Dict[str, Any]]:
        """Get all endpoints matching path prefix.
        
        Args:
            prefix: Path prefix (e.g., '/tasks').
        
        Returns:
            List of matching endpoints.
        """
        return [
            ep for ep in self.get_endpoints()
            if ep.get("path", "").startswith(prefix)
        ]
    
    def get_error_codes(self) -> List[Dict[str, Any]]:
        """Get all error codes from spec.
        
        Returns:
            List of error code definitions.
        """
        return self.spec.get("errorCodes", [])
