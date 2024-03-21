from rest_framework import permissions


class IsAuthorOrModeratorAndAdmin(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        pass


class AdminOrReadOnly(permissions.BasePermission):
    """Админ или только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))
        )
