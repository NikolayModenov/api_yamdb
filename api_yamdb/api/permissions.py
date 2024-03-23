from rest_framework import permissions
from reviews.models import MODERATOR, ADMIN


class IsAdmin(permissions.BasePermission):
    """
    Разрешает доступ только администраторам.
    """

    def has_permission(self, request, view):
        return (
            not request.user.is_authenticated
            or request.user.role == ADMIN or request.user.is_staff
        )


class AdminOrReadOnly(permissions.BasePermission):
    """Админ или только чтение."""

    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS)
            or (request.user.is_authenticated and request.user.role == ADMIN)
        )


class IsAuthorOrModeratorAndAdmin(permissions.IsAuthenticatedOrReadOnly):
    """
    Проверка прав доступа к объекту.
    Пользователь имеет доступ, если он является автором объекта, модератором
    или администратором.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role in (ADMIN, MODERATOR)
        )
