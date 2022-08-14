from django.contrib.auth import authenticate, get_user_model
from djoser.serializers import TokenCreateSerializer
from rest_framework import serializers

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    """ Serializer for registration new users. """

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}


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

    password = serializers.CharField(
        max_length=150,
        style={'input_type': 'password'},
    )
    email = serializers.EmailField(
        max_length=254,
        style={'input_type': 'email'},
    )

    def validate(self, attrs):
        password = attrs.get('password')
        email = attrs.get('email')
        self.user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password,
        )
        if not self.user:
            self.user = User.objects.filter(email=email).first()
            if self.user and not self.user.check_password(password):
                self.fail('invalid_credentials')
        if self.user and self.user.is_active:
            return attrs
        self.fail('invalid_credentials')


class PasswordSerializer(serializers.Serializer):
    """ Serializer for changing password. """

    new_password = serializers.CharField(
        max_length=150,
        style={"input_type": "password"},
        label="New password",
    )
    current_password = serializers.CharField(
        max_length=150,
        style={"input_type": "password"},
        label="New password",
    )

    def validate(self, attrs):
        if attrs.get('new_password') == attrs.get('current_password'):
            raise serializers.ValidationError(
                "new password couldn't be the same"
            )
        return attrs
