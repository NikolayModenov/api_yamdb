from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from api.filters import TitleFilter
from api.mixins import CreateListDestroyViewSet
from api.permissions import AdminOrReadOnly
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, ReviewSerializer,
    TitleEditingSerializer, TitleViewingSerializer
)
from api.viewsets import AbstractReviewCommentViewSet
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """Вьюсет для произведений."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('rating')
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        """Определяет сериализатор в зависимости от типа запроса."""
        if self.action in ('list', 'retrieve'):
            return TitleViewingSerializer
        return TitleEditingSerializer


class ReviewViewSet(AbstractReviewCommentViewSet):
    """Представление для обработки запросов к отзывам на заголовки."""
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(AbstractReviewCommentViewSet):
    """Представление для обработки запросов комментария к отзыву."""
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review,
                                 pk=self.kwargs.get('review_id'),
                                 title_id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)
