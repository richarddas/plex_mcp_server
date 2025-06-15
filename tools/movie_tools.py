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
            },
            {
    "name": "get_movie_details",
    "description": "Get detailed information about a specific movie including cast, crew, and metadata",
    "inputSchema": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Movie title to get details for"}
        },
        "required": ["title"]
    }
},
{
    "name": "search_by_actor", 
    "description": "Find all movies featuring a specific actor",
    "inputSchema": {
        "type": "object",
        "properties": {
            "actor_name": {"type": "string", "description": "Actor name to search for"},
            "limit": {"type": "integer", "description": "Maximum results", "default": 20}
        },
        "required": ["actor_name"]
    }
},
{
    "name": "find_similar_by_metadata",
    "description": "Find movies similar to a reference movie based on shared metadata (genres, directors, actors, decade)",
    "inputSchema": {
        "type": "object", 
        "properties": {
            "reference_movie": {"type": "string", "description": "Movie to find similar movies to"},
            "similarity_factors": {
                "type": "array",
                "items": {"type": "string", "enum": ["genres", "directors", "actors", "decade"]},
                "description": "What factors to consider for similarity",
                "default": ["genres", "directors", "actors", "decade"]
            }
        },
        "required": ["reference_movie"]
    }
},
{
    "name": "search_multi_criteria",
    "description": "Search movies using multiple criteria simultaneously (genres, directors, actors, year range, rating)",
    "inputSchema": {
        "type": "object",
        "properties": {
            "genres": {"type": "array", "items": {"type": "string"}, "description": "List of genres to match"},
            "directors": {"type": "array", "items": {"type": "string"}, "description": "List of directors to match"},
            "actors": {"type": "array", "items": {"type": "string"}, "description": "List of actors to match"},
            "year_range": {"type": "array", "items": {"type": "integer"}, "description": "Year range as [start_year, end_year]"},
            "min_rating": {"type": "number", "description": "Minimum rating threshold"},
            "limit": {"type": "integer", "description": "Maximum results", "default": 30}
        }
    }
},
{
    "name": "get_genre_combinations",
    "description": "Get movies grouped by genre combinations to understand library patterns",
    "inputSchema": {
        "type": "object",
        "properties": {
            "limit": {"type": "integer", "description": "Maximum genre combinations to return", "default": 20}
        }
    }
},
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
    
    @staticmethod
    def get_movie_details(title: str) -> Dict[str, Any]:
        """Get detailed information about a specific movie including cast and crew"""
        try:
            section = plex_client.get_movie_library()
            results = section.search(title=title, limit=1)
            
            if not results:
                return {"error": f"Movie '{title}' not found"}
            
            movie = results[0]
            
            # Get detailed metadata
            details = {
                "title": movie.title,
                "year": getattr(movie, 'year', None),
                "rating": getattr(movie, 'rating', None),
                "duration": getattr(movie, 'duration', None),
                "summary": getattr(movie, 'summary', ''),
                "genres": [g.tag for g in getattr(movie, 'genres', [])],
                "directors": [d.tag for d in getattr(movie, 'directors', [])],
                "writers": [w.tag for w in getattr(movie, 'writers', [])],
                "actors": [{"name": a.tag, "role": getattr(a, 'role', '')} for a in getattr(movie, 'roles', [])[:10]],  # Top 10 actors
                "countries": [c.tag for c in getattr(movie, 'countries', [])],
                "studio": getattr(movie, 'studio', None),
                "content_rating": getattr(movie, 'contentRating', None),
                "tags": [t.tag for t in getattr(movie, 'tags', [])]
            }
            
            return {"movie_details": details}
        except Exception as e:
            logger.error(f"Error getting movie details: {e}")
            return {"error": str(e)}

    @staticmethod
    def search_by_actor(actor_name: str, limit: int = 20) -> Dict[str, Any]:
        """Find movies featuring a specific actor"""
        try:
            section = plex_client.get_movie_library()
            results = section.search(actor=actor_name, limit=limit)
            movies = []
            
            for movie in results:
                # Get the actor's role in this movie
                actor_role = ""
                for role in getattr(movie, 'roles', []):
                    if actor_name.lower() in role.tag.lower():
                        actor_role = getattr(role, 'role', '')
                        break
                
                movies.append({
                    "title": movie.title,
                    "year": getattr(movie, 'year', None),
                    "rating": getattr(movie, 'rating', None),
                    "genres": [g.tag for g in getattr(movie, 'genres', [])],
                    "actor_role": actor_role
                })
            
            return {"movies": movies, "actor": actor_name, "total": len(movies)}
        except Exception as e:
            logger.error(f"Error searching by actor: {e}")
            return {"error": str(e)}

    @staticmethod
    def find_similar_by_metadata(reference_movie: str, similarity_factors: List[str] = None) -> Dict[str, Any]:
        """Find movies similar to a reference movie based on metadata overlap"""
        if similarity_factors is None:
            similarity_factors = ["genres", "directors", "actors", "decade"]
        
        try:
            # Get details of the reference movie
            ref_details = MovieTools.get_movie_details(reference_movie)
            if "error" in ref_details:
                return ref_details
            
            ref_data = ref_details["movie_details"]
            section = plex_client.get_movie_library()
            
            # Get all movies to compare against
            all_movies = section.all()
            similar_movies = []
            
            for movie in all_movies:
                if movie.title.lower() == reference_movie.lower():
                    continue  # Skip the reference movie itself
                
                similarity_score = 0
                similarity_reasons = []
                
                # Genre similarity
                if "genres" in similarity_factors:
                    movie_genres = [g.tag for g in getattr(movie, 'genres', [])]
                    genre_overlap = set(ref_data["genres"]) & set(movie_genres)
                    if genre_overlap:
                        similarity_score += len(genre_overlap) * 2
                        similarity_reasons.append(f"Shared genres: {', '.join(genre_overlap)}")
                
                # Director similarity
                if "directors" in similarity_factors:
                    movie_directors = [d.tag for d in getattr(movie, 'directors', [])]
                    director_overlap = set(ref_data["directors"]) & set(movie_directors)
                    if director_overlap:
                        similarity_score += len(director_overlap) * 3
                        similarity_reasons.append(f"Shared directors: {', '.join(director_overlap)}")
                
                # Actor similarity
                if "actors" in similarity_factors:
                    movie_actors = [a.tag for a in getattr(movie, 'roles', [])]
                    ref_actors = [a["name"] for a in ref_data["actors"]]
                    actor_overlap = set(ref_actors) & set(movie_actors)
                    if actor_overlap:
                        similarity_score += len(actor_overlap)
                        similarity_reasons.append(f"Shared actors: {', '.join(list(actor_overlap)[:3])}")
                
                # Decade similarity
                if "decade" in similarity_factors:
                    ref_year = ref_data.get("year")
                    movie_year = getattr(movie, 'year', None)
                    if ref_year and movie_year:
                        ref_decade = (ref_year // 10) * 10
                        movie_decade = (movie_year // 10) * 10
                        if ref_decade == movie_decade:
                            similarity_score += 1
                            similarity_reasons.append(f"Same decade ({movie_decade}s)")
                
                # Only include movies with some similarity
                if similarity_score > 0:
                    similar_movies.append({
                        "title": movie.title,
                        "year": getattr(movie, 'year', None),
                        "rating": getattr(movie, 'rating', None),
                        "genres": [g.tag for g in getattr(movie, 'genres', [])],
                        "similarity_score": similarity_score,
                        "similarity_reasons": similarity_reasons
                    })
            
            # Sort by similarity score
            similar_movies.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            return {
                "reference_movie": reference_movie,
                "similar_movies": similar_movies[:20],  # Top 20 most similar
                "similarity_factors": similarity_factors,
                "total_found": len(similar_movies)
            }
        
        except Exception as e:
            logger.error(f"Error finding similar movies: {e}")
            return {"error": str(e)}

    @staticmethod
    def search_multi_criteria(genres: List[str] = None, directors: List[str] = None, 
                            actors: List[str] = None, year_range: tuple = None, 
                            min_rating: float = None, limit: int = 30) -> Dict[str, Any]:
        """Search movies using multiple criteria simultaneously"""
        try:
            section = plex_client.get_movie_library()
            all_movies = section.all()
            matching_movies = []
            
            for movie in all_movies:
                matches = True
                match_reasons = []
                
                # Genre filter
                if genres:
                    movie_genres = [g.tag.lower() for g in getattr(movie, 'genres', [])]
                    genre_matches = [g for g in genres if g.lower() in movie_genres]
                    if not genre_matches:
                        matches = False
                    else:
                        match_reasons.append(f"Genres: {', '.join(genre_matches)}")
                
                # Director filter
                if directors and matches:
                    movie_directors = [d.tag.lower() for d in getattr(movie, 'directors', [])]
                    director_matches = [d for d in directors if d.lower() in movie_directors]
                    if not director_matches:
                        matches = False
                    else:
                        match_reasons.append(f"Directors: {', '.join(director_matches)}")
                
                # Actor filter
                if actors and matches:
                    movie_actors = [a.tag.lower() for a in getattr(movie, 'roles', [])]
                    actor_matches = [a for a in actors if a.lower() in movie_actors]
                    if not actor_matches:
                        matches = False
                    else:
                        match_reasons.append(f"Actors: {', '.join(actor_matches)}")
                
                # Year range filter
                if year_range and matches:
                    movie_year = getattr(movie, 'year', None)
                    if not movie_year or not (year_range[0] <= movie_year <= year_range[1]):
                        matches = False
                    else:
                        match_reasons.append(f"Year: {movie_year}")
                
                # Rating filter
                if min_rating and matches:
                    movie_rating = getattr(movie, 'rating', None)
                    if not movie_rating or movie_rating < min_rating:
                        matches = False
                    else:
                        match_reasons.append(f"Rating: {movie_rating}")
                
                if matches:
                    matching_movies.append({
                        "title": movie.title,
                        "year": getattr(movie, 'year', None),
                        "rating": getattr(movie, 'rating', None),
                        "genres": [g.tag for g in getattr(movie, 'genres', [])],
                        "directors": [d.tag for d in getattr(movie, 'directors', [])],
                        "match_reasons": match_reasons
                    })
                    
                    if len(matching_movies) >= limit:
                        break
            
            return {
                "movies": matching_movies,
                "search_criteria": {
                    "genres": genres,
                    "directors": directors, 
                    "actors": actors,
                    "year_range": year_range,
                    "min_rating": min_rating
                },
                "total": len(matching_movies)
            }
        
        except Exception as e:
            logger.error(f"Error in multi-criteria search: {e}")
            return {"error": str(e)}

    @staticmethod
    def get_genre_combinations(limit: int = 20) -> Dict[str, Any]:
        """Get movies grouped by genre combinations to understand library patterns"""
        try:
            section = plex_client.get_movie_library()
            all_movies = section.all()
            genre_combos = {}
            
            for movie in all_movies:
                genres = [g.tag for g in getattr(movie, 'genres', [])]
                if len(genres) > 1:
                    # Sort genres to normalize combinations
                    combo = " + ".join(sorted(genres))
                    if combo not in genre_combos:
                        genre_combos[combo] = []
                    
                    genre_combos[combo].append({
                        "title": movie.title,
                        "year": getattr(movie, 'year', None),
                        "rating": getattr(movie, 'rating', None)
                    })
            
            # Sort by number of movies in each combination
            sorted_combos = sorted(
                genre_combos.items(), 
                key=lambda x: len(x[1]), 
                reverse=True
            )[:limit]
            
            return {
                "genre_combinations": [
                    {
                        "genres": combo,
                        "count": len(movies),
                        "movies": movies[:5]  # Show first 5 movies as examples
                    }
                    for combo, movies in sorted_combos
                ]
            }
        
        except Exception as e:
            logger.error(f"Error getting genre combinations: {e}")
            return {"error": str(e)}