from rest_framework.viewsets import ModelViewSet
from django.db.models import Avg
from reviews.models import Category, Genre, Title
from django_filters.rest_framework import DjangoFilterBackend
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleViewingSerializer, TitleEditingSerializer,)
from api.permissions import AdminOrReadOnly
from api.mixins import CreateListDestroyViewSet


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year',)

    def get_serializer_class(self):
        """Определяет сериализатор в зависимости от типа запроса."""
        if self.request.method == 'GET':
            return TitleViewingSerializer
        return TitleEditingSerializer
