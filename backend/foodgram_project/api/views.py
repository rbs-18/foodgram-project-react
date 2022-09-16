from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import (
    Favorite, Ingredient, Recipe, ShoppingCart, Subscription, Tag,
)
from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    IngredientSerializer, RecipeCreateSerializer, RecipeSerializer,
    ShortRecipeSerializer, SubscriptionSerializer, TagSerializer,
)

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ Viewset for Tag model. """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Viewset for Tag model. """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """ Viewset for Recipe model. """

    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = LimitPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

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

    def _form_shopping_list(self, cart):
        need_to_buy = dict()

        for cart_object in cart:
            ingredient_queryset = cart_object.recipe.ingredients_list.all()
            for ingredient in ingredient_queryset:
                if ingredient.ingredient.name not in need_to_buy:
                    need_to_buy[ingredient.ingredient.name] = {
                        'measurement_unit':
                        ingredient.ingredient.measurement_unit,
                        'amount': 0,
                    }
                need_to_buy[ingredient.ingredient.name]['amount'] += (
                    ingredient.amount
                )

        return [
            f"{index}. {name} - {need_to_buy[name]['amount']} "
            f"{need_to_buy[name]['measurement_unit']}\n"
            for index, name in enumerate(need_to_buy)
        ]

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """ Download recipes list from shopping cart. """

        cart = ShoppingCart.objects.filter(user=request.user)

        shopping_list = self._form_shopping_list(cart)

        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename=shopping_list.txt'
        )
        return response


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


class ShoppingCartView(APIView):
    """ View for shopping cart. """

    permission_classes = [IsAuthenticated]

    def post(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)

        if (ShoppingCart.objects.filter(user=user, recipe=recipe).exists()):
            return Response(
                {
                    'errors':
                    'Shopping cart error. The recipe already in cart!'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        ShoppingCart.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(
            recipe, context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        cart = ShoppingCart.objects.filter(
            user=request.user, recipe=recipe,
        )

        if not cart:
            return Response(
                {
                    'errors':
                    "Shopping cart error. The recipe isn't in cart!",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
