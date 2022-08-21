from rest_framework import filters, viewsets

from recipes.models import Ingredient, Tag
from .serializers import IngredientSerializer, TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ Viewset for Tag model. """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None  #TODO определиться позже, где определять класс пагинации


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Viewset for Tag model. """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None  # TODO определиться позже, где определять класс пагинации
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
