from rest_framework import viewsets
from .permissions import IsAuthorOrModeratorAndAdmin


class AbstractReviewCommentViewSet(viewsets.ModelViewSet):
    """
    Абстрактная Класс представления для работы комментариев, отзыв.
    Поддерживает методы GET, POST, PATCH и DELETE.
    """
    permission_classes = (IsAuthorOrModeratorAndAdmin,)
    http_method_names = ('get', 'post', 'patch', 'delete')
