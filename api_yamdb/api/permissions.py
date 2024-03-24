from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Разрешает доступ только администраторам.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class AdminOrReadOnly(IsAdmin):
    """Админ или только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
        ) or super().has_permission(request, view)


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
