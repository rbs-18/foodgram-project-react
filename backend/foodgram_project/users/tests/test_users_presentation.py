from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (APIClient, APIRequestFactory, APITestCase,
                                 force_authenticate)

from ..serializers import UserSerializer
from .errors import TestErrors

User = get_user_model()


class UsersPresentation(APITestCase):
    """ Tests for checking User presentation. """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user = User.objects.create(
            email='test_user1@user.ru',
            username='test_user1',
            first_name='user1',
            last_name='test1',
        )

        cls.user.set_password('123hjk123')

        cls.authenticated_user = APIClient()
        cls.authenticated_user.force_authenticate(user=cls.user)

    def test_get_list_users(self):
        """ Getting list of users. """

        response = self.client.get(reverse('user-list'))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            TestErrors.INVALID_STATUS_CODE,
        )
        self.assertEqual(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'email': self.user.email,
                        'id': self.user.id,
                        'username': self.user.username,
                        'first_name': self.user.first_name,
                        'last_name': self.user.last_name,
                        'is_subscribed': False,
                    },
                ]
            },
            TestErrors.INAVLID_USER_DATA,
        )

    def test_single_user(self):
        """ Getting single user. """

        response = self.client.get(
            reverse('user-detail', kwargs={'pk': self.user.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            TestErrors.INVALID_STATUS_CODE,
        )
        self.assertEqual(
            response.json(),
            {
                'email': self.user.email,
                'id': self.user.id,
                'username': self.user.username,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'is_subscribed': False,
            },
            TestErrors.INAVLID_USER_DATA,
        )

    def test_current_user_without_authentication(self):
        """ Getting current user. """

        response = self.client.get(reverse('user-detail', args=['me']))
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            TestErrors.INVALID_STATUS_CODE,
        )

    def test_current_user(self):
        """ Getting current user. """

        response = self.authenticated_user.get(
            reverse('user-detail', args=['me'])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            TestErrors.INVALID_STATUS_CODE,
        )

        factory = APIRequestFactory()
        request = factory.get(reverse('user-detail', args=['me']))
        force_authenticate(request, self.user)
        request.user = self.user
        serializer = UserSerializer(self.user, context={'request': request})

        self.assertEqual(
            response.json(),
            serializer.data,
            TestErrors.INAVLID_USER_DATA,
        )
