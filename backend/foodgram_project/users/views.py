from django.contrib.auth import get_user_model
from djoser.views import TokenCreateView
from rest_framework import viewsets

from .serializers import CreateUserSerializer, UserSerializer, CustomTokenCreateSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ Viewset for User model. """

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        return UserSerializer


class CustomTokenCreateView(TokenCreateView):
    """ Custom viewset for creating token. """

    queryset = User.objects.all()
    serializer_class = CustomTokenCreateSerializer
