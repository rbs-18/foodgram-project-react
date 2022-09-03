from rest_framework import filters, viewsets, mixins

from recipes.models import Ingredient, Recipe, Tag
from .serializers import (
    IngredientSerializer, RecipeCreateSerializer,
    TagSerializer, RecipeSerializer
)


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


class RecipeViewSet(viewsets.ModelViewSet):
    """ Viewset for Recipe model. """

    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
