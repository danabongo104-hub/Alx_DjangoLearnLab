from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
# Create your models here.
class Notification(models.Model):
    # WHo recieves the notification
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    # Who triggered the notification
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actor_notifications')
    # What happened? (e.g., 'liked', 'commented', 'followed')
    verb = models.CharField(max_length=255)

    # Generic relation to the object that triggered the notification
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('content_type', 'object_id')

    timestamp = models.DateTimeField(auto_now_add=True)

    # Has the recipient read the notification?
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timesamp']  # newest first by default

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.actor.username} {self.verb}"