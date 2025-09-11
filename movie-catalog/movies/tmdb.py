# movies/tmdb.py
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.core.cache import cache
from typing import Optional, Dict, Any

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
TMDB_BASE = "https://api.themoviedb.org/3"

# HTTP session with retries
_session = requests.Session()
retries = Retry(total=3, backoff_factor=0.5, status_forcelist=(500,502,503,504))
_session.mount("https://", HTTPAdapter(max_retries=retries))

def _get(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if not TMDB_API_KEY:
        raise RuntimeError("TMDB_API_KEY is not set in environment")
    url = f"{TMDB_BASE}{path}"
    p = params.copy() if params else {}
    p["api_key"] = TMDB_API_KEY
    try:
        resp = _session.get(url, params=p, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as exc:
        # Log exception in real app
        raise RuntimeError(f"TMDb API request failed: {exc}") from exc

def get_trending(media_type: str = "movie", time_window: str = "day") -> Dict[str, Any]:
    """Trending movies. Cached by default at view layer."""
    return _get(f"/trending/{media_type}/{time_window}")

def get_movie_details(movie_id: int) -> Dict[str, Any]:
    return _get(f"/movie/{movie_id}", params={"append_to_response": "credits,images"})

def search_movies(query: str, page: int = 1):
    return _get("/search/movie", params={"query": query, "page": page})
