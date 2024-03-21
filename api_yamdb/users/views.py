from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.views import APIView

from .models import YamdbUser
from .serializers import AuthUserSerializer, TokenSerializer


def generate_and_send_confirmation_code(request):
    """Генерация кода подтверждения и его отправка."""
    user = get_object_or_404(YamdbUser, username=request.data.get('username'))
    send_mail(
        'Yamdb. Confirmation code',
        f'confirmation_code: {default_token_generator.make_token(user)}',
        'a@yambd.face',
        [user.email]
    )


# class SignUpView(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     permission_classes = (AllowAny,)
#     queryset = YamdbUser.objects.all()
#     serializer_class = AuthUserSerializer


class SignUpView(APIView):
    """Вью-функция для регистрации и подтверждения по почте."""
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

    def perform_create(self, serializer):
        """Сохраняет сериализатор с указанием роли пользователя."""
        serializer.save(confirmation_code=)


class TokenView(TokenViewBase):
    """Вьюсет для получения токена."""
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer

    # def perform_create(self, serializer):
    #     # """Сохраняет сериализатор с указанием роли пользователя."""
    #     serializer.save(confirmation_code=self.request.user.confirmation_code)


    # def post(self, request):
    #     """POST-запрос на получение JWT-токена."""
    #     serializer = TokenSerializer(data=self.request.data)
    #     serializer.is_valid(raise_exception=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    


# from django.contrib.auth.validators import UnicodeUsernameValidator
# from django.core.exceptions import ValidationError
# from django.core.mail import send_mail
# from django.shortcuts import render
# from rest_framework import status
# from rest_framework import viewsets
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.mixins import CreateModelMixin
# from rest_framework.response import Response
# from rest_framework.decorators import api_view

# from .models import YamdbUser

# from .serializers import AuthUserSerializer

# MESAGE = 'сообщение с кодом подтверждения отправлено отправлено.'


# # class AuthUserViewSet(viewsets.ModelViewSet):
# #     queryset = YamdbUser.objects.all()
# #     serializer_class = AuthUserSerializer


# @api_view(['POST'])
# def send_confirmation_code_email(request):
#     serializer = AuthUserSerializer(data=request.data)
#     if serializer.is_valid():
#         send_mail(
#             subject='Тема письма',
#             message='Текст сообщения',
#             # from_email='from@example.com',
#             recipient_list=['to@example.com'],
#             fail_silently=True,
#         )
#         return Response(
#             template_name=MESAGE, status=status.HTTP_200_OK
#         )
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
