from django.test import TestCase
from oauth2_provider.models import Application, AccessToken, RefreshToken
from django.urls import reverse
from django.utils import timezone
from tests import User

class OAuth2TokenEndpointTests(TestCase):
    def setUp(self):
        # URLs
        self.LOGIN_URL = reverse('access-token')
        self.TOKEN_REFRESH_URL = self.LOGIN_URL

        # Test user data
        self.valid_login_data = {
            'email': 'test@example.com',
            'password': 'strongpassword123',
        }

        # Create a test user
        self.user = User.objects.create_user(**self.valid_login_data)

        # Create a test application
        self.application = Application.objects.create(
            name='Test Application',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            user=self.user,
            client_id='test_id',
            client_secret='test_idss',
        )

        # Payload for token requests
        self.payload = {
            'username': self.valid_login_data['email'],
            'password': self.valid_login_data['password'],
            'grant_type': 'password',
            'client_id': 'test_id',
            'client_secret': 'test_idss',
        }

    def test_refresh_access_token(self):

        refresh_token_value = self.client.post(self.LOGIN_URL, self.payload).json()['refresh_token']
        # Use the refresh token to obtain a new access token
        refresh_payload = self.payload | {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token_value,
        }

        refresh_response = self.client.post(self.TOKEN_REFRESH_URL, refresh_payload)
        self.assertEqual(refresh_response.status_code, 200)

        # Check if the response contains the required fields
        self.assertIn('access_token', refresh_response.json())

        # Retrieve the new access token from the database
        access_token_value = refresh_response.json()['access_token']
        token_obj = AccessToken.objects.get(token=access_token_value)

        # Verify that the new access token is associated with the correct user and application
        self.assertEqual(token_obj.user, self.user)
        self.assertEqual(token_obj.application, self.application)

    def test_expired_refresh_token(self):

        # Extract the refresh token from the response
        refresh_token_value = self.client.post(self.LOGIN_URL, self.payload).json()['refresh_token']

        # Expire the refresh token
        expired_refresh_token = RefreshToken.objects.get(token=refresh_token_value)
        expired_refresh_token.revoked = timezone.now() - timezone.timedelta(days=1)
        expired_refresh_token.save()

        # Attempt to refresh the access token with the expired refresh token
        refresh_payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token_value,
            'client_id': 'test_id',
            'client_secret': 'test_idss',
        }

        refresh_response = self.client.post(self.TOKEN_REFRESH_URL, refresh_payload)
        self.assertEqual(refresh_response.status_code, 400)

    def test_invalid_refresh_token(self):
        # Attempt to refresh the access token with an invalid refresh token
        refresh_payload = {
            'refresh_token': 'invalid_refresh_token',
            'client_id': 'test_id',
            'client_secret': 'test_idss',
        }

        refresh_response = self.client.post(self.TOKEN_REFRESH_URL, refresh_payload)
        self.assertEqual(refresh_response.status_code, 400)

    def test_missing_refresh_token(self):
        # Attempt to refresh the access token without providing a refresh token
        refresh_payload = {
            'grant_type': 'refresh_token',
            'client_id': 'test_id',
            'client_secret': 'test_idss',
        }

        refresh_response = self.client.post(self.TOKEN_REFRESH_URL, refresh_payload)
        self.assertEqual(refresh_response.status_code, 400)

        # Check if the response contains an error message
        self.assertIn('error', refresh_response.json())
        self.assertEqual('invalid_request', refresh_response.json()['error'])
        self.assertIn('error_description', refresh_response.json())
        self.assertEqual('Missing refresh token parameter.', refresh_response.json()['error_description'])
