from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenViewBase

from api.filters import TitleFilter
from api.mixins import CreateListDestroyViewSet
from api.permissions import AdminOrReadOnly, IsAuthorOrModeratorAndAdmin, IsAdmin
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, ReviewSerializer,
    TitleEditingSerializer, TitleViewingSerializer, UserRegistrationSerializer,
    TokenSerializer, AuthUserSerializer
)
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

    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Метод \'PUT\' не разрешен."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        title = self.get_title()
        serializer.save(title=title)
        self.update_title_rating(title)
        return Response(serializer.data)

    def update_title_rating(self, title):
        """Обновляет рейтинг заголовка на основе отзывов."""
        reviews = Review.objects.filter(title=title)
        average_score = (
            sum(review.score for review in reviews) / reviews.count()
        ) if reviews.count() > 0 else 0
        title.rating = round(average_score, 2)
        title.save()


class CommentViewSet(viewsets.ModelViewSet):
    """
    Представление для обработки запросов комментария к отзыву.
    Поддерживает методы GET, POST, PATCH и DELETE.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorAndAdmin,)

    def get_review(self):
        return get_object_or_404(
            Review, id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)

    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Метод \'PUT\' не разрешен."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(review=self.get_review())
        return Response(serializer.data)


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
