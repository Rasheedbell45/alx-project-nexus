from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL  # uses default or custom user

class Post(models.Model):
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    content = models.TextField()
    media_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Post {self.pk} by {self.author}"


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Comment {self.pk} on Post {self.post.pk}"


class Interaction(models.Model):
    LIKE = "LIKE"
    SHARE = "SHARE"

    INTERACTION_CHOICES = [
        (LIKE, "Like"),
        (SHARE, "Share"),
    ]

    post = models.ForeignKey(Post, related_name="interactions", on_delete=models.CASCADE)
    actor = models.ForeignKey(User, related_name="interactions", on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["post", "interaction_type"]),
            models.Index(fields=["created_at"]),
        ]
        unique_together = ('post', 'actor', 'interaction_type')  # prevents duplicate likes/shares by same user

    def __str__(self):
        return f"{self.interaction_type} by {self.actor} on {self.post.pk}"
