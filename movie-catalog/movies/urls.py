# movies/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrendingMoviesView, MovieRecommendationsView, FavoriteMovieViewSet

router = DefaultRouter()
router.register(r"user/favorites", FavoriteMovieViewSet, basename="user-favorites")

urlpatterns = [
    path("movies/trending/", TrendingMoviesView.as_view(), name="movies-trending"),
    path("movies/recommendations/", MovieRecommendationsView.as_view(), name="movies-recommendations"),
    path("", include(router.urls)),
]
