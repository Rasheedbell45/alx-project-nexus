# movies/models.py
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, related_name="favorite_movies", on_delete=models.CASCADE)
    movie_id = models.IntegerField(db_index=True)  # TMDb movie id
    title = models.CharField(max_length=500, blank=True)
    poster_path = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie_id")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} favorite {self.movie_id}"
