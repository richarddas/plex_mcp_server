"""Plex server client and connection management"""

import logging
from typing import Optional
from plexapi.server import PlexServer
from plexapi.exceptions import PlexApiException

from config import config

logger = logging.getLogger(__name__)

class PlexClient:
    """Plex server client wrapper"""
    
    def __init__(self):
        self._server: Optional[PlexServer] = None
        self._connect()
    
    def _connect(self) -> None:
        """Connect to Plex server"""
        try:
            self._server = PlexServer(config.PLEX_URL, config.PLEX_TOKEN)
            logger.info(f"Connected to Plex: {self._server.friendlyName}")
        except PlexApiException as e:
            logger.error(f"Failed to connect to Plex: {e}")
            raise
    
    @property
    def server(self) -> PlexServer:
        """Get Plex server instance"""
        if self._server is None:
            self._connect()
        return self._server
    
    @property
    def server_name(self) -> str:
        """Get Plex server friendly name"""
        return self.server.friendlyName
    
    def get_movie_library(self):
        """Get the first movie library section"""
        for section in self.server.library.sections():
            if section.type == 'movie':
                return section
        raise ValueError("No movie section found in Plex library")
    
    def get_tv_library(self):
        """Get the first TV library section"""
        for section in self.server.library.sections():
            if section.type == 'show':
                return section
        raise ValueError("No TV section found in Plex library")

# Global Plex client instance
plex_client = PlexClient()
