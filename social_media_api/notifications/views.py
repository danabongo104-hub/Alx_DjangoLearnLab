from django.shortcuts import render
"""
notifications/views.py

WHY ListAPIView?
    Notifications are read-only from the client's perspective —
    they're generated server-side. Users fetch them, they don't
    create them directly.

WHY mark as read on GET?
    Standard notification UX — viewing your notifications marks
    them as read automatically, like most social media platforms.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    GET /api/notifications/
    Returns all notifications for the authenticated user,
    unread ones first.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Unread first, then by newest timestamp
        return Notification.objects.filter(recipient=self.request.user).order_by('is_read', '-timestamp')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Mark all as read after fetching
        queryset.filter(is_read=False).update(is_read=True)

        return Response(serializer.data)
