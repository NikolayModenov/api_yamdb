from rest_framework import permissions


class AdminAuthorOrReadOnly(permissions.BasePermission):
    """Админ/автор или только чтение."""

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser
            or request.user.is_admin
            or obj == request.user
        )


# class AdminOnly(permissions.BasePermission):
#     """Только админ."""

#     def has_permission(self, request, view):
#         return (
#             request.user.is_authenticated
#             and (
#                 request.user.is_superuser
#                 or request.user.is_admin
#                 or request.user.is_staff
#             )
#         )


class AdminOrReadOnly(permissions.BasePermission):
    """Админ или только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))
        )


# class AuthorOrModeratorsOrReadOnly(permissions.BasePermission):
#     """Админ/модератор/автор или только чтение."""

#     def has_object_permission(self, request, view, obj):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_superuser
#             or request.user.is_admin
#             or request.user.is_moderator
#             or obj.author == request.user
#         )


# class AnonReadOnly(permissions.BasePermission):
#     """Анонимный пользователь и только безопасные запросы."""

#     def has_permission(self, request, view):
#         return (
#             request.method in permissions.SAFE_METHODS
#         )


# class AdminOrSuperuserOnly(permissions.BasePermission):
#     """Админ/суперпользователь или только чтение."""

#     def has_permission(self, request, view):
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user.is_superuser
#                 or request.user.is_admin)

#     def has_object_permission(self, request, view, obj):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_superuser
#             or request.user.is_admin
#         )