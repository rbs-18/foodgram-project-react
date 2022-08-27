from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from djoser.views import TokenCreateView
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    CreateUserSerializer, CustomTokenCreateSerializer,
    PasswordSerializer, UserSerializer
)

User = get_user_model()


class CreateRetrieveListViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """ ViewSet for GET, POST requests. """

    pass


class UserViewSet(CreateRetrieveListViewSet):
    """ Viewset for User model. """

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        return UserSerializer

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    def perform_update(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise NotAuthenticated
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def set_password(self, request):
        user = request.user
        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid():
            if (
                not user.check_password(
                    serializer.data.get('current_password')
                )
            ):
                return Response(
                    {'current_password': ['Wrong password.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenCreateView(TokenCreateView):
    """ Custom viewset for creating token. """

    serializer_class = CustomTokenCreateSerializer
