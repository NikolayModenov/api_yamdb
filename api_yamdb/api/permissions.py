from rest_framework import permissions


class IsAuthorOrModeratorAndAdmin(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        pass
