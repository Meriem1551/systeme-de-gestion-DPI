from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admins to perform certain actions.
    """
    def has_permission(self, request, view):
        # Check if the requesting user is an admin
        return request.user and request.user.is_staff and request.user.is_superuser