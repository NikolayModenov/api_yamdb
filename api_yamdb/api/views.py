from rest_framework.viewsets import ModelViewSet
from django.db.models import Avg
from reviews.models import Category, Genre, Title, Review
from django_filters.rest_framework import DjangoFilterBackend
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleViewingSerializer, TitleEditingSerializer, ReviewSerializer, CommentSerializer)
from api.permissions import AdminOrReadOnly, IsAuthorOrModeratorAndAdmin
from api.mixins import CreateListDestroyViewSet
from api.filters import TitleFilter
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status

from rest_framework.response import Response



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


# class ReviewViewSet(viewsets.ModelViewSet):
#     serializer_class = ReviewSerializer

#     def get_title(self):
#         return get_object_or_404(Title, pk=self.kwargs.get('titles_id'))

#     def get_queryset(self):
#         return self.get_title().reviews.all()

#     def perform_create(self, serializer):
#         title = self.get_title()
#         serializer.save(title=title)
#         self.update_title_rating(title)

#     def perform_update(self, serializer):
#         title = self.get_title()
#         serializer.save(title=title)
#         self.update_title_rating(title)

#     def perform_destroy(self, instance):
#         instance.delete()
#         self.update_title_rating(self.get_title())

#     def update_title_rating(self, title):
#         reviews = Review.objects.filter(title=title)
#         average_score = (sum(review.score for review in reviews)
#                          / reviews.count()) if reviews.count() > 0 else 0
#         title.raiting = round(average_score, 2)
#         title.save()
    

class ReviewViewSet(viewsets.ModelViewSet):
    """
    Представление для обработки запросов к отзывам на заголовки.

    Поддерживает методы GET, POST, PATCH и DELETE.
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeratorAndAdmin,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(title=title, author=self.request.user)
        self.update_title_rating(title)

    def perform_destroy(self, instance):
        title = instance.title
        instance.delete()
        self.update_title_rating(title)

    def update(self, request, *args, kwargs):
        return Response({'detail': 'Метод "PUT" не разрешен.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        title = self.get_title()
        serializer.save(title=title)
        self.update_title_rating(title)
        return Response(serializer.data)

    def update_title_rating(self, title):
        """Обновляет рейтинг заголовка на основе отзывов."""
        reviews = Review.objects.filter(title=title)
        average_score = (sum(review.score for review in reviews)
                         / reviews.count()) if reviews.count() > 0 else 0
        title.rating = round(average_score, 2)
        title.save()


# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer

#     def get_review(self):
#         return get_object_or_404(Review,
#                                  id=self.kwargs.get('review_id'),
#                                  title_id=self.kwargs.get('titles_id'))

#     def get_queryset(self):
#         return self.get_review().comments.all()

#     def perform_create(self, serializer):
#         serializer.save(review=self.get_review())

class CommentViewSet(viewsets.ModelViewSet):
    """
    Представление для обработки запросов комментария к отзыву.

    Поддерживает методы GET, POST, PATCH и DELETE.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorAndAdmin,)

    def get_review(self):
        return get_object_or_404(Review,
                                 id=self.kwargs.get('review_id'),
                                 title_id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)

    def update(self, request, *args, kwargs):
        return Response({'detail': 'Метод "PUT" не разрешен.'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(review=self.get_review())
        return Response(serializer.data)
