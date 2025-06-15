"""Movie-related MCP tools for Plex"""

import logging
from typing import Dict, Any, List
from plexapi.exceptions import PlexApiException

from plex_client import plex_client

logger = logging.getLogger(__name__)

class MovieTools:
    """Movie-related MCP tools"""
    
    @staticmethod
    def get_tool_definitions() -> List[Dict[str, Any]]:
        """Get MCP tool definitions for movies"""
        return [
            {
                "name": "get_library_stats",
                "description": "Get overall movie library statistics including total movies, top genres, and directors",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "list_all_movies",
                "description": "List all movies in the library with pagination",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Number of movies to return", "default": 100},
                        "offset": {"type": "integer", "description": "Starting position", "default": 0}
                    }
                }
            },
            {
                "name": "search_movies",
                "description": "Search for movies by title",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Movie title to search for"},
                        "limit": {"type": "integer", "description": "Maximum results", "default": 10}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "search_by_genre",
                "description": "Find movies by genre (e.g., Drama, Comedy, Sci-Fi)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "genre": {"type": "string", "description": "Genre to search for"},
                        "limit": {"type": "integer", "description": "Maximum results", "default": 20}
                    },
                    "required": ["genre"]
                }
            },
            {
                "name": "search_by_director",
                "description": "Find movies by director name",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "director": {"type": "string", "description": "Director name to search for"},
                        "limit": {"type": "integer", "description": "Maximum results", "default": 20}
                    },
                    "required": ["director"]
                }
            },
            {
                "name": "search_by_year_range",
                "description": "Find movies within a specific year range",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "start_year": {"type": "integer", "description": "Starting year"},
                        "end_year": {"type": "integer", "description": "Ending year"},
                        "limit": {"type": "integer", "description": "Maximum results", "default": 30}
                    },
                    "required": ["start_year", "end_year"]
                }
            },
            {
                "name": "get_all_genres",
                "description": "Get all available genres in the library",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_all_directors",
                "description": "Get all directors in the library",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_recent_movies",
                "description": "Get recently added movies",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Maximum results", "default": 10}
                    }
                }
            }
        ]
    
    @staticmethod
    def list_all_movies(limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get all movies in library with pagination"""
        try:
            section = plex_client.get_movie_library()
            all_movies = section.all()
            total = len(all_movies)
            movies = all_movies[offset:offset+limit]
            
            result = []
            for movie in movies:
                result.append({
                    "title": movie.title,
                    "year": getattr(movie, 'year', None),
                    "rating": getattr(movie, 'rating', None),
                    "genres": [g.tag for g in getattr(movie, 'genres', [])],
                    "directors": [d.tag for d in getattr(movie, 'directors', [])],
                    "summary": MovieTools._truncate_summary(getattr(movie, 'summary', ''))
                })
            
            return {
                "movies": result,
                "total": total,
                "offset": offset,
                "limit": limit,
                "has_more": offset + limit < total
            }
        except Exception as e:
            logger.error(f"Error listing movies: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def search_movies(query: str, limit: int = 10) -> Dict[str, Any]:
        """Search for movies by title"""
        try:
            section = plex_client.get_movie_library()
            results = section.search(title=query, limit=limit)
            movies = []
            for movie in results:
                movies.append({
                    "title": movie.title,
                    "year": getattr(movie, 'year', None),
                    "rating": getattr(movie, 'rating', None),
                    "summary": MovieTools._truncate_summary(getattr(movie, 'summary', ''), 200),
                    "genres": [g.tag for g in getattr(movie, 'genres', [])],
                    "directors": [d.tag for d in getattr(movie, 'directors', [])]
                })
            return {"movies": movies, "total": len(movies)}
        except Exception as e:
            logger.error(f"Error searching movies: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def search_by_genre(genre: str, limit: int = 20) -> Dict[str, Any]:
        """Find movies by genre"""
        try:
            section = plex_client.get_movie_library()
            results = section.search(genre=genre, limit=limit)
            movies = []
            for movie in results:
                movies.append({
                    "title": movie.title,
                    "year": getattr(movie, 'year', None),
                    "rating": getattr(movie, 'rating', None),
                    "genres": [g.tag for g in getattr(movie, 'genres', [])],
                    "directors": [d.tag for d in getattr(movie, 'directors', [])]
                })
            return {"movies": movies, "genre": genre, "total": len(movies)}
        except Exception as e:
            logger.error(f"Error searching by genre: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def search_by_director(director: str, limit: int = 20) -> Dict[str, Any]:
        """Find movies by director"""
        try:
            section = plex_client.get_movie_library()
            results = section.search(director=director, limit=limit)
            movies = []
            for movie in results:
                movies.append({
                    "title": movie.title,
                    "year": getattr(movie, 'year', None),
                    "rating": getattr(movie, 'rating', None),
                    "genres": [g.tag for g in getattr(movie, 'genres', [])],
                    "directors": [d.tag for d in getattr(movie, 'directors', [])]
                })
            return {"movies": movies, "director": director, "total": len(movies)}
        except Exception as e:
            logger.error(f"Error searching by director: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def search_by_year_range(start_year: int, end_year: int, limit: int = 30) -> Dict[str, Any]:
        """Find movies within a year range"""
        try:
            section = plex_client.get_movie_library()
            all_movies = section.all()
            filtered = []
            for movie in all_movies:
                year = getattr(movie, 'year', None)
                if year and start_year <= year <= end_year:
                    filtered.append({
                        "title": movie.title,
                        "year": year,
                        "rating": getattr(movie, 'rating', None),
                        "genres": [g.tag for g in getattr(movie, 'genres', [])],
                        "directors": [d.tag for d in getattr(movie, 'directors', [])]
                    })
                    if len(filtered) >= limit:
                        break
            
            return {
                "movies": filtered,
                "year_range": f"{start_year}-{end_year}",
                "total": len(filtered)
            }
        except Exception as e:
            logger.error(f"Error searching by year range: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def get_all_genres() -> Dict[str, Any]:
        """Get all available genres in the library"""
        try:
            section = plex_client.get_movie_library()
            genres = set()
            all_movies = section.all()
            for movie in all_movies:
                for genre in getattr(movie, 'genres', []):
                    genres.add(genre.tag)
            
            return {"genres": sorted(list(genres))}
        except Exception as e:
            logger.error(f"Error getting genres: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def get_all_directors() -> Dict[str, Any]:
        """Get all directors in the library"""
        try:
            section = plex_client.get_movie_library()
            directors = set()
            all_movies = section.all()
            for movie in all_movies:
                for director in getattr(movie, 'directors', []):
                    directors.add(director.tag)
            
            return {"directors": sorted(list(directors))}
        except Exception as e:
            logger.error(f"Error getting directors: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def get_recent_movies(limit: int = 10) -> Dict[str, Any]:
        """Get recently added movies"""
        try:
            section = plex_client.get_movie_library()
            recent = section.recentlyAdded(maxresults=limit)
            movies = []
            
            for movie in recent:
                movies.append({
                    "title": movie.title,
                    "year": getattr(movie, 'year', None),
                    "added_at": str(movie.addedAt) if hasattr(movie, 'addedAt') else None,
                    "genres": [g.tag for g in getattr(movie, 'genres', [])],
                    "directors": [d.tag for d in getattr(movie, 'directors', [])],
                    "summary": MovieTools._truncate_summary(getattr(movie, 'summary', ''))
                })
            
            return {"recent_movies": movies}
        except Exception as e:
            logger.error(f"Error getting recent movies: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def get_library_stats() -> Dict[str, Any]:
        """Get overall library statistics"""
        try:
            section = plex_client.get_movie_library()
            all_movies = section.all()
            total_movies = len(all_movies)
            
            # Count by decade
            decades = {}
            genres = {}
            directors = {}
            
            for movie in all_movies:
                # Decade analysis
                year = getattr(movie, 'year', None)
                if year:
                    decade = (year // 10) * 10
                    decades[f"{decade}s"] = decades.get(f"{decade}s", 0) + 1
                
                # Genre analysis
                for genre in getattr(movie, 'genres', []):
                    genres[genre.tag] = genres.get(genre.tag, 0) + 1
                
                # Director analysis
                for director in getattr(movie, 'directors', []):
                    directors[director.tag] = directors.get(director.tag, 0) + 1
            
            # Top 10 of each
            top_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)[:10]
            top_directors = sorted(directors.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return {
                "total_movies": total_movies,
                "decades": decades,
                "top_genres": top_genres,
                "top_directors": top_directors
            }
        except Exception as e:
            logger.error(f"Error getting library stats: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def _truncate_summary(summary: str, max_length: int = 150) -> str:
        """Truncate summary text"""
        if not summary:
            return ""
        return summary[:max_length] + '...' if len(summary) > max_length else summary
    