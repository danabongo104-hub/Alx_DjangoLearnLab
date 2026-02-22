from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """
    - Authenticated users: read any post/comment (GET, HEAD, OPTIONS)
    - Author only: edit or delete (PUT, PATCH, DELETE)
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read-only methods allowed for any authenticated user
        if request.method in SAFE_METHODS:
            return True
        # Write methods require ownership
        return obj.author == request.user