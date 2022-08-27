from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class CreateUserTest(APITestCase):
    """ Testing of endpoints, connection with User model. """

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
        response = self.client.post(
            reverse('user-list'),
            valid_data,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            'Wrong response status',
        )
        self.assertEqual(
            User.objects.count(),
            object_count + 1,
            'New object not created in database',
        )
        last_object = User.objects.latest('pk')
        self.assertEqual(
            (
                last_object.email,
                last_object.username,
                last_object.first_name,
                last_object.last_name,
            ),
            (
                'test_user@user.ru',
                'test_user',
                'user',
                'test',
            ),
            "Invalid user data",
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
            }
        ]

        for data in invalid_data:
            with self.subTest(data=data):
                response = self.client.post(
                    reverse('user-list'),
                    data,
                )
                self.assertEqual(
                    response.status_code, status.HTTP_400_BAD_REQUEST
                )
