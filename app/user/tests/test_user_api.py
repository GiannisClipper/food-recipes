from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_vaild(self):
        """Test creating a user with valid payload"""

        payload = {
            'email': 'test@email.org',
            'password': 'test123',
            'name': 'test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists"""

        payload = {
            'email': 'test@email.org',
            'password': 'test123',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be at least 6 characters"""

        payload = {
            'email': 'test@email.org',
            'password': 'test',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        test_user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(test_user_exists)

    def test_create_token_valid(self):
        """Test that a token is created for a user"""
        payload = {'email': 'test@email.org', 'password': 'test123'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials(self):
        """Test that a token is not created when credentials are invalid"""
        payload = {'email': 'test@email.org', 'password': 'test123'}
        create_user(**payload)
        payload['password'] = 'test1234'
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_user_not_exists(self):
        """Test that a token is not created when user doesn't exist"""
        payload = {'email': 'test@email.org', 'password': 'test123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload = {'email': 'anything', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
