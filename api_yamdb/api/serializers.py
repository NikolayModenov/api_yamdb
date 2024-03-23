from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


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
    category = CategorySerializer(read_only=True,)
    genre = GenreSerializer(many=True, read_only=True,)
    rating = serializers.SerializerMethodField(read_only=True,)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        obj = obj.reviews.all().aggregate(rating=Avg('score'))
        return obj['rating']


class TitleEditingSerializer(serializers.ModelSerializer):
    """Сериализатор произведения в режиме создания/редактирования."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'author', 'pub_date')

    def validate(self, attrs):
        title = get_object_or_404(
            Title,
            pk=self.context['view'].kwargs.get('title_id')
        )
        request = self.context['request']
        if request.method == 'POST':
            if Review.objects.filter(title=title,
                                     author=request.user).exists():
                raise serializers.ValidationError("Вы уже оставляли отзыв.")

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
