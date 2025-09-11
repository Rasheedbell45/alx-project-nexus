# movies/serializers.py
from rest_framework import serializers
from .models import FavoriteMovie

class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = ["id", "movie_id", "title", "poster_path", "created_at"]
        read_only_fields = ["id", "created_at"]
