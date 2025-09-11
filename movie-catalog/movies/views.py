# movies/views.py
from django.core.cache import cache
from rest_framework import viewsets, status, permissions, generics, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .tmdb import get_trending, get_movie_details, search_movies
from .serializers import FavoriteMovieSerializer
from .models import FavoriteMovie
from django.conf import settings

TRENDING_CACHE_KEY = "tmdb_trending_{media}_{window}"
RECOMMEND_CACHE_KEY = "tmdb_recommend_{movie_id}"

CACHE_TTL = int(getattr(settings, "TMDB_CACHE_TTL", 60 * 15))  # 15 minutes default

class TrendingMoviesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        media = request.query_params.get("media", "movie")
        window = request.query_params.get("window", "day")
        cache_key = TRENDING_CACHE_KEY.format(media=media, window=window)
        data = cache.get(cache_key)
        if data is None:
            try:
                data = get_trending(media_type=media, time_window=window)
            except RuntimeError as exc:
                return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
            cache.set(cache_key, data, timeout=CACHE_TTL)
        return Response(data)

class MovieRecommendationsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        movie_id = request.query_params.get("movie_id")
        if not movie_id:
            return Response({"detail": "movie_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        cache_key = RECOMMEND_CACHE_KEY.format(movie_id=movie_id)
        data = cache.get(cache_key)
        if data is None:
            # simple approach: use /movie/{id}/recommendations endpoint of TMDb
            try:
                data = get_movie_details(movie_id=int(movie_id))
                # Optionally call recommendations endpoint:
                from .tmdb import _get
                recs = _get(f"/movie/{movie_id}/recommendations")
                data = {"movie": data, "recommendations": recs}
            except RuntimeError as exc:
                return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
            cache.set(cache_key, data, timeout=CACHE_TTL)
        return Response(data)

# User favorites: list/create/delete
class FavoriteMovieViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteMovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteMovie.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Validate duplicates unique_together will also protect but handle gracefully
        serializer.save(user=self.request.user)
