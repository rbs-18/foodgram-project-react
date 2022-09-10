from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .errors import TestErrors

User = get_user_model()


class CreateUserTest(APITestCase):
    """ Testing of endpoints, connection with creation of User object. """

    def test_registration_new_user(self):
        """
        Test registration of new user with valid data
        from api/users/ endpoint.
        """

        object_count = User.objects.count()
        valid_data = {
            'email': 'test_user@user.ru',
            'username': 'test_user',
            'first_name': 'user',
            'last_name': 'test',
            'password': 'testpassword11',
        }

        response = self.client.post(reverse('user-list'), valid_data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            TestErrors.INVALID_STATUS_CODE,
        )
        self.assertEqual(
            User.objects.count(),
            object_count + 1,
            TestErrors.NOT_CREATED,
        )

        last_user = User.objects.latest('pk')
        self.assertEqual(
            (
                last_user.email,
                last_user.username,
                last_user.first_name,
                last_user.last_name,
            ),
            (
                valid_data['email'],
                valid_data['username'],
                valid_data['first_name'],
                valid_data['last_name'],
            ),
            TestErrors.INAVLID_USER_DATA,
        )
        self.assertTrue(
            last_user.check_password(valid_data['password']),
            TestErrors.INVALID_PASSWORD
        )

    def test_invalid_data_registration(self):
        """
        Test registration of new user with invalid data
        from api/users/ endpoint.
        """

        invalid_data = [
            {
                'email': 'test_user@user.ru',
                'username': 'test_user',
                'first_name': 'user',
                'last_name': 'test',
            },
            {
                'email': 'test_user@user.ru',
                'username': 'test_user',
                'first_name': 'user',
                'password': 'testpassword11',
            },
            {
                'email': 'test_user@user.ru',
                'username': 'test_user',
                'last_name': 'test',
                'password': 'testpassword11',
            },
            {
                'email': 'test_user@user.ru',
                'first_name': 'user',
                'last_name': 'test',
                'password': 'testpassword11',
            },
            {
                'username': 'test_user',
                'first_name': 'user',
                'last_name': 'test',
                'password': 'testpassword11',
            },
            {
                'username': 'test_user',
                'email': 'test_user@user.ru',
                'first_name': 'user',
                'last_name': 'test',
                'password': '1',
            }
        ]

        for data in invalid_data:
            with self.subTest(data=data):
                response = self.client.post(reverse('user-list'), data)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                    TestErrors.INVALID_STATUS_CODE,
                )
