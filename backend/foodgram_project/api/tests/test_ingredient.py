from random import randint

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from recipes.models import Ingredient
from ..serializers import IngredientSerializer


class GetIngredientsTest(APITestCase):
    """ Test module for GET list of ingredients and single object. """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.ingredient_1 = Ingredient.objects.create(
            name='Test ingredient 1',
            measurement_unit='unit',
        )
        cls.ingredient_2 = Ingredient.objects.create(
            name='Unit test ingredient 2',
            measurement_unit='unit',
        )

    def test_amount_ingredients(self):
        """ Test amount of created objects. """

        self.assertEqual(
            Ingredient.objects.count(),
            2,
            "Incorrect creation objects",
        )

    def test_get_all_ingredients(self):
        """ Test list endpount response. """

        response = self.client.get(reverse('ingredient-list'))

        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            'Wrong response status',
        )
        self.assertEqual(
            response.json(),
            serializer.data,
            'Invalid response data',
        )

    def test_get_single_ingredient(self):
        """ Test single object endpount response. """

        response = self.client.get(
            reverse('ingredient-detail', kwargs={'pk': self.ingredient_1.pk})
        )

        ingredient = Ingredient.objects.get(pk=self.ingredient_1.pk)
        serializer = IngredientSerializer(ingredient)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            'Wrong response status',
        )
        self.assertEqual(
            response.json(),
            serializer.data,
            'Invalid response data',
        )

    def _generate_random_index(self) -> int:
        """ Generate invalid index. """

        valid_indexes = (self.ingredient_1.pk, self.ingredient_2.pk)
        invalid_index = 3
        while invalid_index in valid_indexes:
            invalid_index = randint(4, 100)
        return invalid_index

    def test_get_invalid_single_ingredient(self):
        """ Test single endpount with invalid parameter response. """

        invalid_index = self._generate_random_index()
        response = self.client.get(
            reverse('ingredient-detail', kwargs={'pk': invalid_index})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            'Wrong response status',
        )

    def test_search_filter(self):
        """ Test search filter for endpoint. """

        start_with = 'Test'
        url = f"{reverse('ingredient-list')}?search={start_with}"

        filtred_objects = Ingredient.objects.filter(
            name__startswith=start_with
        )
        serializer = IngredientSerializer(filtred_objects, many=True)
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            'Wrong response status',
        )
        self.assertEqual(
            response.json(),
            serializer.data,
            'Invalid response data',
        )
