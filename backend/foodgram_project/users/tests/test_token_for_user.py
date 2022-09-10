from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .errors import TestErrors

User = get_user_model()


class TokenForUserTest(APITestCase):

    """ Tests for checking Token creation. """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create(
            email='test_user@user.ru',
            username='test_user',
            first_name='user',
            last_name='test',
        )
        password = 'testpassword11'
        cls.data = {'password': password, 'email': cls.user.email}

        cls.user.set_password(password)
        cls.user.save()

    def test_get_token(self):
        """ Test getting token. """

        response = self.client.post(
            reverse('users:custom_login'),
            self.data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            TestErrors.INVALID_STATUS_CODE,
        )
        self.assertIsNotNone(
            response.json().get('auth_token'),
            TestErrors.INVALID_RESPONSE_DATA
        )

    def test_delete_token(self):
        """ Test deleting token. """

        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('users:logout'))

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            TestErrors.INVALID_STATUS_CODE
        )

    def test_delete_token_without_authentication(self):
        """ Test deleting token unauthorized user. """

        response = self.client.post(reverse('users:logout'))

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            TestErrors.INVALID_STATUS_CODE,
        )
