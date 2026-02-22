from django.db import models
from django.conf import settings
# Create your models here.

class Post(models.Model):
    # ForeignKey to the custom user — always use settings.AUTH_USER_MODEL,
    # never hardcode 'auth.User', so the reference works even if the user
    # model changes.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # newest first by default

    def __str__(self):
        return f"{self.title} by {self.author.username}"


class Comment(models.Model):
    # A comment belongs to exactly one post
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',  # post.comments.all() → all comments on a post
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',  # user.comments.all() → all comments by a user
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']  # oldest first for threaded readability

    def __str__(self):
        return f"Comment by {self.author.username} on '{self.post.title}'"

