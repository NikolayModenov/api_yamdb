from rest_framework import serializers
from reviews.models import Category, Genre, Title
from django.db.models import Avg

from reviews.models import Review, Comment


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
    category = CategorySerializer(
        read_only=True,
    )
    genre = GenreSerializer(
        many=True,
        read_only=True,
    )
    rating = serializers.SerializerMethodField(
        read_only=True,
    )

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
# from rest_framework.serializers import UniqueTogetherValidator


# class ReviewSerializer(serializers.ModelSerializer):
#     # title = serializers.HiddenField(
#     #     default=serializers.SerializerMethodField())

#     class Meta:
#         model = Review
#         fields = ('id', 'text', 'score', 'pub_date')
#         read_only_fields = ('title',)
#         # validators = [
#         #     UniqueTogetherValidator(
#         #         queryset=Review.objects.all(),
#         #         fields=('title', 'author'),
#         #         message='Вы уже оставляли отзыв.'
#         #     )
#         # ]

#     # def get_title(self, obj):
#     #     return self.context['view'].kwargs.get('titles_id')


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review.

    Этот сериализатор преобразует объекты модели Review в формат JSON.
    """
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'author', 'pub_date')
        read_only_fields = ('title',)

    def create(self, validated_data):
        title = validated_data.get('title')
        author = validated_data.get('author')

        if title and Review.objects.filter(title=title,
                                           author=author).exists():
            raise serializers.ValidationError("Вы уже оставляли отзыв.")

        return super().create(validated_data)



# class CommentSerializer(serializers.ModelSerializer):
#     # author = serializers.SlugRelatedField(slug_field='username',
#     #                                       read_only=True)

#     class Meta:
#         model = Comment
#         fields = ('id', 'text', 'pub_date')
#         read_only_fields = ('review',)


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.

    Этот сериализатор преобразует объекты модели Comment в формат JSON.
    """
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)
