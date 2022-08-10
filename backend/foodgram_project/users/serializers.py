from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import TokenCreateSerializer

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    """ Serializer for registration new users. """

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for User model. """

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            # 'is_subscribed'
        )


class CustomTokenCreateSerializer(TokenCreateSerializer):
    """ Custom serializer for geting token. """

    class Meta:
        model = User
        fields = ('password', 'email')
