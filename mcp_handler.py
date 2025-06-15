"""MCP message handling and routing"""

import logging
from typing import Dict, Any

from tools import MovieTools
from tools.tv_tools import TVTools

logger = logging.getLogger(__name__)

class MCPHandler:
    """Handle MCP JSON-RPC messages"""
    
    def __init__(self):
        self.movie_tools = MovieTools()
        self.tv_tools = TVTools()
        
        # Build tool registry
        self.tools = {}
        self._register_tools()
    
    def _register_tools(self):
        """Register all available tools"""
        # Movie tools
        movie_methods = {
            'list_all_movies': self.movie_tools.list_all_movies,
            'search_movies': self.movie_tools.search_movies,
            'search_by_genre': self.movie_tools.search_by_genre,
            'search_by_director': self.movie_tools.search_by_director,
            'search_by_year_range': self.movie_tools.search_by_year_range,
            'get_all_genres': self.movie_tools.get_all_genres,
            'get_all_directors': self.movie_tools.get_all_directors,
            'get_recent_movies': self.movie_tools.get_recent_movies,
            'get_library_stats': self.movie_tools.get_library_stats,
            'get_movie_details': self.movie_tools.get_movie_details,
            'search_by_actor': self.movie_tools.search_by_actor,
            'find_similar_by_metadata': self.movie_tools.find_similar_by_metadata,
            'search_multi_criteria': self.movie_tools.search_multi_criteria,
            'get_genre_combinations': self.movie_tools.get_genre_combinations,
        }
        self.tools.update(movie_methods)
        
        # TV tools (future)
        # tv_methods = {...}
        # self.tools.update(tv_methods)
    
    def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP JSON-RPC messages"""
        try:
            method = message.get("method")
            params = message.get("params", {})
            msg_id = message.get("id")
            
            logger.info(f"Handling MCP message: {method}")
            
            if method == "initialize":
                return self._handle_initialize(msg_id)
            elif method == "tools/list":
                return self._handle_tools_list(msg_id)
            elif method == "tools/call":
                return self._handle_tools_call(msg_id, params)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32601, "message": f"Unknown method: {method}"}
                }
        
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {"code": -32603, "message": str(e)}
            }
    
    def _handle_initialize(self, msg_id: int) -> Dict[str, Any]:
        """Handle initialize message"""
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "plex-mcp-server",
                    "version": "1.0.0"
                }
            }
        }
    
    def _handle_tools_list(self, msg_id: int) -> Dict[str, Any]:
        """Handle tools/list message"""
        tools = []
        tools.extend(MovieTools.get_tool_definitions())
        tools.extend(TVTools.get_tool_definitions())
        
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": tools}
        }
    
    def _handle_tools_call(self, msg_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call message"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        logger.info(f"Calling tool: {tool_name} with args: {arguments}")
        
        if tool_name not in self.tools:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
            }
        
        try:
            # Call the tool method
            tool_method = self.tools[tool_name]
            result = tool_method(**arguments)
            
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"{result}"
                        }
                    ]
                }
            }
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32603, "message": str(e)}
            }

# Global MCP handler instance
mcp_handler = MCPHandler()
