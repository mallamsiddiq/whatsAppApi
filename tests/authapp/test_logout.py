from django.test import TestCase
from oauth2_provider.models import Application
from django.urls import reverse
from . import User

class OAuth2TokenEndpointTests(TestCase):
    def setUp(self):
        # URLs
        self.LOGIN_URL = reverse('access-token')
        self.LOGOUT_URL = reverse('revoke-token')  # Assuming 'logout' is the name of the logout view URL
        self.PROTECTED_URL = reverse('protected')  # Assuming 'protected' is the name of the protected view URL

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

    def test_logout(self):
        # Extract the access token from the response
        access_token_value = self.client.post(self.LOGIN_URL, self.payload).json()['access_token']
        protected_response = self.client.get(self.PROTECTED_URL, HTTP_AUTHORIZATION=f'Bearer {access_token_value}')
        self.assertEqual(protected_response.status_code, 200)

        # Make a request to the logout URL with the access token
        payload = {
            'grant_type': 'password',
            'client_id': 'test_id',
            'client_secret': 'test_idss',
            'token': access_token_value
        }
        logout_response = self.client.post(self.LOGOUT_URL, payload)
        self.assertEqual(logout_response.status_code, 200)

        # Attempt to use the logged-out access token to access a protected resource
        protected_response = self.client.get(self.PROTECTED_URL, HTTP_AUTHORIZATION=f'Bearer {access_token_value}')
        self.assertEqual(protected_response.status_code, 401)