from random import randint

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from recipes.models import Tag
from ..serializers import TagSerializer


class GetTagsTest(APITestCase):
    """ Test module for GET list of tags and single object. """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.tag_1 = Tag.objects.create(
            name='Test tag 1',
            color='#FF0000',
            slug='test1',
        )
        cls.tag_2 = Tag.objects.create(
            name='Test tag 2',
            color='#0000FF',
            slug='test2',
        )

    def test_amount_tags(self):
        """ Test amount of created objects. """

        self.assertEqual(Tag.objects.count(), 2, "Incorrect creation objects")

    def test_get_all_tags(self):
        """ Test list endpount response. """

        response = self.client.get(reverse('tag-list'))

        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)

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

    def test_get_single_tag(self):
        """ Test single object endpount response. """

        response = self.client.get(
            reverse('tag-detail', kwargs={'pk': self.tag_1.pk})
        )

        tag = Tag.objects.get(pk=self.tag_1.pk)
        serializer = TagSerializer(tag)

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

        valid_indexes = (self.tag_1.pk, self.tag_2.pk)
        invalid_index = 3
        while invalid_index in valid_indexes:
            invalid_index = randint(4, 100)
        return invalid_index

    def test_get_invalid_single_tag(self):
        """ Test single endpount with invalid parameter response. """

        invalid_index = self._generate_random_index()
        response = self.client.get(
            reverse('tag-detail', kwargs={'pk': invalid_index})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            'Wrong response status',
        )
