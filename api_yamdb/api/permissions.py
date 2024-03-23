from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Разрешает доступ только администраторам.
    """

    def has_permission(self, request, view):
        return (
            not request.user.is_authenticated
            or request.user.role == 'admin' or request.user.is_staff
        )


class AdminOrReadOnly(permissions.BasePermission):
    """Админ или только чтение."""

    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS)
            or (request.user.is_authenticated and request.user.role == "admin")
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
            or request.user.is_admin or request.user.is_moderator
        )
