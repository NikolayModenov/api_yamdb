from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import YamdbUser


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = YamdbUser
        fields = '__all__'


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=250)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(YamdbUser, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                'Неверный код подтверждения.'
            )
        return data
