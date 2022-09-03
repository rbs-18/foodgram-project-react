from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase, APIClient, APIRequestFactory, force_authenticate
)

from .serializers import UserSerializer

User = get_user_model()


class TestErrors:
    """ Possible errors in tests. """

    INVALID_STATUS_CODE = 'Invalid status code'
    INAVLID_USER_DATA = 'Invalid user data'
    NOT_CREATED = 'New object not created in database'
    INVALID_PASSWORD = 'Invalid user password'
    INVALID_RESPONSE_DATA = 'Invalid response data'


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


class TokenForUser(APITestCase):
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


class ChangePassword(APITestCase):
    """ Tests for changing password. """

    TEST_ENDPOINT = reverse('user-detail', args=['set_password'])

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test_user@user.ru',
            username='test_user',
            first_name='user',
            last_name='test',
        )

        self.password = 'testpassword11'
        self.user.set_password(self.password)
        self.user.save()

        self.authenticated_user = APIClient()
        self.authenticated_user.force_authenticate(user=self.user)

    def test_change_password(self):
        """ Changing password with valid data. """

        new_password = '123sad123'
        data = {
            'new_password': new_password,
            'current_password': self.password,
        }

        response = self.authenticated_user.post(self.TEST_ENDPOINT, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            TestErrors.INVALID_STATUS_CODE,
        )
        self.assertTrue(
            self.user.check_password(new_password),
            TestErrors.INVALID_RESPONSE_DATA
        )

    def test_change_password_without_authentication(self):
        """ Changing password without authentication. """

        data = {
            'new_password': '123asd123',
            'current_password': self.password,
        }
        response = self.client.post(self.TEST_ENDPOINT, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            TestErrors.INVALID_STATUS_CODE
        )

    def test_change_password_with_invalid_data(self):
        """ Changing password with invalid data. """
        data = {
            'new_password': self.password,
            'current_password': self.password,
        }
        response = self.authenticated_user.post(self.TEST_ENDPOINT, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            TestErrors.INVALID_STATUS_CODE
        )

        data['new_password'] = '1'
        response = self.authenticated_user.post(self.TEST_ENDPOINT, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            TestErrors.INVALID_STATUS_CODE
        )


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
            TestErrors.INVALID_STATUS_CODE
        )

    def test_current_user(self):
        """ Getting current user. """

        response = self.authenticated_user.get(
            reverse('user-detail', args=['me'])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            TestErrors.INVALID_STATUS_CODE
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
