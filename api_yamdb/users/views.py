from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from api.permissions import IsAdmin
from users.models import YamdbUser
from users.serializers import AuthUserSerializer, TokenSerializer


def generate_and_send_confirmation_code(request):
    """Генерация кода подтверждения и его отправка."""
    user = get_object_or_404(YamdbUser, username=request.data.get('username'))
    send_mail(
        'Yamdb. Confirmation code',
        f'confirmation_code: {default_token_generator.make_token(user)}',
        'a@yambd.face',
        [user.email]
    )


class SignUpView(APIView):
    """Вью-класс для регистрации и подтверждения по почте."""
    permission_classes = (AllowAny,)

    def post(self, request):
        """Обрабатывает POST-запрос для регистрации пользователя."""
        if YamdbUser.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email'),
        ).exists():
            generate_and_send_confirmation_code(request)
            return Response(request.data, status=status.HTTP_200_OK)

        serializer = AuthUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        generate_and_send_confirmation_code(request)
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
        url_path='me'
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
        serializer.validated_data['role'] = request.user.role
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
