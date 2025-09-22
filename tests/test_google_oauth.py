from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from unittest.mock import patch
from finances.models import User

class GoogleOAuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('google_login')  # name this route in urls.py

    @patch('finances.views.id_token.verify_oauth2_token')
    def test_google_login_creates_user(self, mock_verify):
        # Mock Google’s response
        mock_verify.return_value = {
            'sub': '1234567890',
            'email': 'testuser@example.com',
            'name': 'Test User'
        }

        response = self.client.post(self.url, {'token': 'fake-google-token'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.google_id, '1234567890')
        self.assertEqual(user.email, 'testuser@example.com')

    @patch('finances.views.id_token.verify_oauth2_token')
    def test_google_login_existing_user(self, mock_verify):
        # Create user first
        user = User.objects.create(
            google_id='1234567890',
            email='testuser@example.com',
            name='Existing User'
        )

        # Mock Google’s response
        mock_verify.return_value = {
            'sub': '1234567890',
            'email': 'testuser@example.com',
            'name': 'Test User'
        }

        response = self.client.post(self.url, {'token': 'fake-google-token'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)  # still 1, not duplicated

    @patch('finances.views.id_token.verify_oauth2_token')
    def test_google_login_invalid_token(self, mock_verify):
        # Simulate token verification failure
        mock_verify.side_effect = Exception("Invalid token")

        response = self.client.post(self.url, {'token': 'bad-token'}, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
