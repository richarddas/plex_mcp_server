"""TV show-related MCP tools for Plex (future expansion)"""

import logging
from typing import Dict, Any, List

from plex_client import plex_client

logger = logging.getLogger(__name__)

class TVTools:
    """TV show-related MCP tools"""
    
    @staticmethod
    def get_tool_definitions() -> List[Dict[str, Any]]:
        """Get MCP tool definitions for TV shows"""
        # TODO: Implement TV show tools
        return []
    
    # TODO: Add TV show methods like:
    # - list_all_shows()
    # - search_shows()
    # - get_show_seasons()
    # - get_recent_episodes()
    # etc.
