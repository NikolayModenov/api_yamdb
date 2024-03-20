from rest_framework import serializers
from reviews.models import Category, Genre, Title, Comment, Review, User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    class Meta:
        model = Category
        fields = ('name', 'slug', )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра."""

    class Meta:
        model = Genre
        fields = ('name', 'slug', )


class TitleViewingSerializer(serializers.ModelSerializer):
    """Сериализатор произведения в режиме просмотра."""
    # rating
    # read_only=True,
    class Meta:
        model = Title
        fields = '__all__'


class TitleEditingSerializer(serializers.ModelSerializer):
    """Сериализатор произведения в режиме создания/редактирования."""
    # rating
    class Meta:
        model = Title
        fields = '__all__'
