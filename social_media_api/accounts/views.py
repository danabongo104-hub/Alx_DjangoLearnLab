from django.shortcuts import render
"""
accounts/views.py

WHY APIView instead of ViewSet for auth endpoints?
    Register and Login are one-off actions — they don't map to a CRUD
    resource the way Posts or Comments do. APIView gives us precise
    control over the single HTTP method each endpoint handles.

WHY AllowAny on Register and Login?
    These are the entry points to the API. If they required auth the
    user could never get their first token. AllowAny overrides the
    global IsAuthenticated default from settings.py.

WHY RetrieveUpdateAPIView for Profile?
    It provides GET (retrieve) and PATCH/PUT (update) out of the box,
    which is exactly what a profile page needs. We override get_object()
    so it always returns request.user — a user can only see/edit their
    own profile via this endpoint.
"""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegisterSerializer, UserProfileSerializer

User = get_user_model()


class RegisterView(APIView):
    """
    POST /api/accounts/register/
    Public endpoint. Creates a new user and returns their auth token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Return 201 Created (not 200 OK) — a new resource was created
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    POST /api/accounts/login/
    Public endpoint. Validates credentials and returns the user's token.

    WHY get_or_create instead of get?
        Handles the edge case where a user exists but somehow has no token
        (e.g., manually deleted from the DB). Idempotent and safe.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/accounts/profile/  → returns authenticated user's profile
    PUT  /api/accounts/profile/  → full update
    PATCH /api/accounts/profile/ → partial update (preferred for profiles)

    WHY override get_object()?
        We don't need a pk in the URL — the token identifies the user.
        This keeps the URL clean and prevents users from accessing each
        other's profile via this endpoint (they'd need a separate
        "public profile" endpoint for that).
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Always returns the currently authenticated user
        return self.request.user

class FollowView(APIView):
    """
    POST /api/accounts/follow/<user_id>/

    WHY POST and not PUT/PATCH?
        Following someone is an action, not a resource update.
        POST is the correct verb for actions that trigger side effects.

    WHY get_object_or_404?
        If the user_id doesn't exist, return a clean 404 instead of
        crashing with an unhandled exception.

    WHY prevent self-follow?
        Following yourself would pollute your own feed with your own
        posts — it serves no purpose and is confusing UX.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # Get the user to follow or return 404
        user_to_follow = get_object_or_404(User, id=user_id)

        # Can't follow yourself
        if request.user == user_to_follow:
            return Response(
                {'error': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add to following — if already following, this is a no-op
        # (ManyToMany .add() is idempotent, won't create duplicates)
        request.user.following.add(user_to_follow)

        return Response(
            {'message': f'You are now following {user_to_follow.username}.'},
            status=status.HTTP_200_OK
        )


class UnfollowView(APIView):
    """
    POST /api/accounts/unfollow/<user_id>/

    WHY POST and not DELETE?
        We're not deleting a resource at a URL — we're triggering an
        action. POST keeps it consistent with FollowView.

    WHY .remove() instead of .delete()?
        .remove() removes the relationship from the M2M join table.
        .delete() would delete the actual User object — very different!
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)

        if request.user == user_to_unfollow:
            return Response(
                {'error': 'You cannot unfollow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Remove from following — if not following, this is a no-op
        request.user.following.remove(user_to_unfollow)

        return Response(
            {'message': f'You have unfollowed {user_to_unfollow.username}.'},
            status=status.HTTP_200_OK
        )