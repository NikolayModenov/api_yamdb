from django.db import IntegrityError
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import (
    Category, Comment, Genre, Review, Title, YamdbUser, MAX_LENGTH
)
from reviews.validators import validate_username


FIELDS_META = (
    'id',
    'name',
    'year',
    'rating',
    'description',
    'genre',
    'category'
)


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = YamdbUser
        fields = 'username', 'email', 'role', 'first_name', 'last_name', 'bio'


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH, required=True
    )
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(YamdbUser, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError('Неверный код подтверждения.')
        return data


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=MAX_LENGTH, required=True,)
    username = serializers.CharField(
        max_length=MAX_LENGTH, required=True,
        validators=[
            UnicodeUsernameValidator(), validate_username
        ]
    )

    def create(self, validated_data):
        try:
            user, status = YamdbUser.objects.get_or_create(**validated_data)
            return user
        except IntegrityError:
            duplicate_data = (
                validated_data["email"]
                if YamdbUser.objects.filter(
                    email=validated_data["email"]
                ).exists()
                else validated_data["username"]
            )
            raise serializers.ValidationError(
                f'Введённое значение не уникально: {duplicate_data}. '
                'Для регистрации нового пользователя необходимо '
                'ввести уникальные username и email.'
            )


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
    rating = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = Title
        fields = FIELDS_META
        read_only_fields = FIELDS_META


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
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'author', 'pub_date')

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            title = get_object_or_404(
                Title,
                pk=self.context['view'].kwargs.get('title_id')
            )
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
