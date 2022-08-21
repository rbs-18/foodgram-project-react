from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class CreateUserTest(APITestCase):
    """ Testing of endpoints, connection with User model. """

    # @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     cls.user = User.objects.create_user(
    #         email='test_admin@test_admin.ru',
    #         username='test_admin',
    #         first_name='admin'
    #         last_name='test',
    #         password=make_password('AdmiN11'),
    #     )

    def test_registration_new_user(self):
        """ Test registration of new user from api/users/ endpoint. """

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
            'Return status is invalid',
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
            "Object does not match created"
        )
