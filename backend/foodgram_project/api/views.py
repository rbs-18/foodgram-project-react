from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework import filters, viewsets, mixins
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from recipes.models import Ingredient, Recipe, Tag, Subscription
from .serializers import (
    IngredientSerializer, RecipeCreateSerializer,
    TagSerializer, RecipeSerializer, SubscriptionSerializer
)

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ Viewset for Tag model. """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None  # TODO определиться, где определять класс пагинации


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Viewset for Tag model. """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None  # TODO определиться, где определять класс пагинации
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet): # TODO сделать фильтрацию
    """ Viewset for Recipe model. """

    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SubscribeView(APIView):
    """ View for create and delete Subscriptions. """

    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        follower = request.user
        author = get_object_or_404(User, id=user_id)
        serializer = SubscriptionSerializer

        if follower == author:
            return Response(
                {'errors': "Subscribtion error. You can't follow yourself!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            Subscription.objects.filter(
                follower=follower, author=author,
            ).exists()
        ):
            return Response(
                {'errors': 'Subscribtion error. The subscription exists!'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription = Subscription.objects.create(
            follower=follower, author=author,
        )
        serializer = SubscriptionSerializer(
            subscription, context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        subscription = Subscription.objects.filter(
            follower=request.user, author=author,
        )

        if not subscription.exists():
            return Response(
                {
                    'errors':
                    "Subscribtion error. The subscription doesn't exist!",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
