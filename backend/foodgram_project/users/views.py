from django.contrib.auth import get_user_model
from djoser.views import TokenCreateView
from djoser.utils import login_user
from djoser.conf import settings
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
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
        new_user = serializer.save()
        new_user.set_password(serializer.validated_data.get('password'))
        new_user.save()

    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
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

    def _action(self, serializer):
        token = login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data,
            status=status.HTTP_201_CREATED,
        )
