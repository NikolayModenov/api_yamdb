from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from reviews.models import Category, Genre, Title
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAuthorOrReadOnlyPermission


class CategoryViewSet():
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet():
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.all()
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year',)
