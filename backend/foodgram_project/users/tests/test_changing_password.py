from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .errors import TestErrors

User = get_user_model()


class ChangingPassword(APITestCase):
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
            TestErrors.INVALID_RESPONSE_DATA,
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
            TestErrors.INVALID_STATUS_CODE,
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
            TestErrors.INVALID_STATUS_CODE,
        )

        data['new_password'] = '1'
        response = self.authenticated_user.post(self.TEST_ENDPOINT, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            TestErrors.INVALID_STATUS_CODE,
        )
