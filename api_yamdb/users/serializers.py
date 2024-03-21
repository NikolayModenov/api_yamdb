from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

from .models import YamdbUser


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = YamdbUser
        fields = '__all__'


class TokenSerializer(TokenObtainSerializer):
    username_field = YamdbUser.objects.values('username')

    def get_token(cls, user):
        return AccessToken.for_user(user)
