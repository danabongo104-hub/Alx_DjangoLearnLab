from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    # Show usernames instead of raw IDs
    actor_username = serializers.SerializerMethodField()
    target_str = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'actor', 'actor_username',
            'verb', 'target_str',
            'timestamp', 'is_read',
        ]
        read_only_fields = fields

    def get_actor_username(self, obj):
        return obj.actor.username

    def get_target_str(self, obj):
        # Return a string representation of the target object
        if obj.target:
            return str(obj.target)
        return None