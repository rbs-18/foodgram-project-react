from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import filters, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from recipes.models import Favorite, Ingredient, Recipe, Tag, Subscription
from .serializers import (
    IngredientSerializer, RecipeCreateSerializer,
    TagSerializer, RecipeSerializer, SubscriptionSerializer,
    ShortRecipeSerializer,
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


class RecipeViewSet(viewsets.ModelViewSet):  # TODO сделать фильтрацию
    """ Viewset for Recipe model. """

    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        """ Add recipe in favorites. """

        recipe = get_object_or_404(Recipe, pk=pk)

        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            return Response(
                {'errors': 'The recipe is already in favorites'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Favorite.objects.create(user=request.user, recipe=recipe)
        serializer = ShortRecipeSerializer(
            recipe, context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """ Delete recipe from favorite. """

        recipe = get_object_or_404(Recipe, pk=pk)
        favorite = Favorite.objects.filter(user=request.user, recipe=recipe)

        if not favorite:
            return Response(
                {'error': "The recipe isn't in favorites!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeView(APIView):
    """ View for create and delete Subscriptions. """

    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        follower = request.user
        author = get_object_or_404(User, id=user_id)

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

        if not subscription:
            return Response(
                {
                    'errors':
                    "Subscribtion error. The subscription doesn't exist!",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
