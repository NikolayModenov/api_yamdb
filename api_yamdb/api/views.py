from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenViewBase

from api.filters import TitleFilter
from api.permissions import AdminOrReadOnly, IsAdmin
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, ReviewSerializer,
    TitleEditingSerializer, TitleViewingSerializer, UserRegistrationSerializer,
    TokenSerializer, AuthUserSerializer
)
from api.viewsets import AbstractReviewCommentViewSet
from reviews.models import Category, Genre, Review, Title, YamdbUser


BAD_WORD = 'me'


def send_confirmation_code(user, confirmation_code):
    """Генерация кода подтверждения и его отправка."""
    send_mail(
        'Yamdb. Confirmation code',
        f'confirmation_code: {confirmation_code}',
        from_email=None,
        recipient_list=[user.email]
    )


class CategoryGenreBaseViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Вьюсет, позволяющий осуществлять GET, POST и DELETE запросы."""

    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreBaseViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreBaseViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


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
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)


class SignUpView(APIView):
    """Вью-класс для регистрации и подтверждения по почте."""
    permission_classes = (AllowAny,)

    def post(self, request):
        """Обрабатывает POST-запрос для регистрации пользователя."""
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(
            YamdbUser, username=request.data.get('username')
        )
        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code(user, confirmation_code)
        return Response(request.data, status=status.HTTP_200_OK)


class TokenView(TokenViewBase):
    """Вьюсет для получения токена."""
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer


class UserListViewSet(viewsets.ModelViewSet):
    '''Вьюсет для пользователя'''
    queryset = YamdbUser.objects.all()
    serializer_class = AuthUserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'delete', 'patch']
    lookup_field = 'username'

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path=BAD_WORD
    )
    def get_current_user_info(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @get_current_user_info.mapping.patch
    def update_current_user_info(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
