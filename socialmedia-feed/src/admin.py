from django.contrib import admin
from .models import Post, Comment, Interaction

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Interaction)
