"""Configuration management for Plex MCP Server"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Plex settings
    PLEX_URL: str = os.getenv('PLEX_URL', 'http://localhost:32400')
    PLEX_TOKEN: Optional[str] = os.getenv('PLEX_TOKEN')
    
    # Server settings
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '8000'))
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration"""
        if not cls.PLEX_TOKEN:
            raise ValueError("PLEX_TOKEN environment variable is required")

# Global config instance
config = Config()
