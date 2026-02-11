from rest_framework import permissions

class ReadOnlyOrWrite (permissions.BasePermission):
    """
    Custom permission to only allow read-only access for unauthenticated users,
    and write access for authenticated users.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to authenticated users.
        return request.user and request.user.is_authenticated