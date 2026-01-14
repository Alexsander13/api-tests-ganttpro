"""Configuration module for GanttPRO API tests.

Loads and validates environment variables required for API testing.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for API testing."""
    
    # Required
    BASE_URL: str = os.getenv("BASE_URL", "https://api.ganttpro.com/v1.0")
    API_KEY: Optional[str] = os.getenv("API_KEY")
    
    # Optional IDs for endpoint tests
    TASK_ID: Optional[str] = os.getenv("TASK_ID")
    PROJECT_ID: Optional[str] = os.getenv("PROJECT_ID")
    COMMENT_ID: Optional[str] = os.getenv("COMMENT_ID")
    TIMELOG_ID: Optional[str] = os.getenv("TIMELOG_ID")
    LINK_ID: Optional[str] = os.getenv("LINK_ID")
    ATTACHMENT_ID: Optional[str] = os.getenv("ATTACHMENT_ID")
    RESOURCE_ID: Optional[str] = os.getenv("RESOURCE_ID")
    USER_ID: Optional[str] = os.getenv("USER_ID")
    
    @classmethod
    def validate(cls) -> None:
        """Validate that required configuration is present.
        
        Raises:
            ValueError: If required configuration is missing.
        """
        if not cls.API_KEY:
            raise ValueError(
                "API_KEY is required. Please set it in your .env file. "
                "Copy .env.example to .env and fill in your credentials."
            )
    
    @classmethod
    def get_auth_headers(cls) -> dict:
        """Get authentication headers for API requests.
        
        Returns:
            Dictionary with authentication headers.
        """
        return {
            "X-API-Key": cls.API_KEY or "",
            "Accept": "application/json"
        }


# Validate configuration on module import
try:
    Config.validate()
except ValueError as e:
    # Allow import but warn - tests will handle missing config
    print(f"Warning: {e}")
