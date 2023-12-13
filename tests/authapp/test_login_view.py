from django.test import TestCase
from oauth2_provider.models import Application, AccessToken
from django.urls import reverse
from django.utils import timezone

from . import User

class RefreshTokenTests(TestCase):
    def setUp(self):
        # Create a test user
        self.LOGIN_URL = reverse('access-token')
        self.PROTECTED_URL = reverse('protected')
        
        self.valid_login_data = {
            'email': 'test@example.com',
            'password': 'strongpassword123',
        }

        self.admin_login_data = {
            'email': 'admin@example.com',
            'password': 'strongpassword123',
        }

        self.user = User.objects.create_user(**self.valid_login_data)
        self.admin_user = User.objects.create_superuser(**self.admin_login_data)

        # Create a test application
        self.application = Application.objects.create(
            name='Test Application',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            user=self.admin_user,
            client_id = 'test_id',
            client_secret = 'test_idss',
        )

        self.payload = {
            'username':self.valid_login_data['email'],
            'password':self.valid_login_data['password'],
            'grant_type': 'password',
            'client_id': 'test_id',
            'client_secret': 'test_idss',
        }

    def test_access_token_request(self):

        response = self.client.post(self.LOGIN_URL, self.payload)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the required fields
        self.assertIn('access_token', response.json())
        self.assertIn('refresh_token', response.json())

        # Retrieve the access token from the database
        access_token_value = response.json()['access_token']
        access_token = AccessToken.objects.get(token=access_token_value)

        # Verify that the access token is associated with the correct user and application
        self.assertEqual(access_token.user, self.user)
        self.assertEqual(access_token.application, self.application)

    def test_authenticated_request(self):
        response = self.client.get(self.PROTECTED_URL, HTTP_AUTHORIZATION=f"Bearer {'Invalid access_token_value'}")
        self.assertEqual(response.status_code, 401)

        # Make a request to obtain the access token
        access_token_value = self.client.post(self.LOGIN_URL, self.payload).json()['access_token']
        # Use the access token to authenticate a request to a protected resource
        response = self.client.get(self.PROTECTED_URL, HTTP_AUTHORIZATION=f'Bearer {access_token_value}')
        self.assertEqual(response.status_code, 200)

    def test_expired_refresh_token(self):

        # Extract the refresh token from the response
        access_token = self.client.post(self.LOGIN_URL, self.payload).json()['access_token']
        # Expire the refresh token
        expired_token_obj = AccessToken.objects.get(token=access_token)
        expired_token_obj.expires = timezone.now() - timezone.timedelta(days=1)
        expired_token_obj.save()

        response = self.client.get(self.PROTECTED_URL, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 401)

    def test_invalid_access_token_request(self):
        # Send an invalid request to the token endpoint
        self.payload.update({
            'password': 'wrongpassword',  # Use an incorrect password
        })

        response = self.client.post(self.LOGIN_URL, self.payload)
        self.assertEqual(response.status_code, 400)  # Unauthorized

        # Check if the response contains an error message
        self.assertIn('error', response.json())
        self.assertIn('error_description', response.json())

    def test_invalid_grant_type(self):
        # Test when an invalid grant type is provided
        self.payload.update({
            'grant_type': 'invalid_grant_type',
        })

        response = self.client.post(self.LOGIN_URL, self.payload)
        self.assertEqual(response.status_code, 400)  # Bad Request

        # Check if the response contains an error message
        self.assertEqual('unsupported_grant_type', response.json()['error'])

    def test_missing_required_invalid_client(self):
        # Test when required parameters are missing
        data = self.valid_login_data | {
            'grant_type': 'password',
        }

        response = self.client.post(self.LOGIN_URL, data)
        self.assertEqual(response.status_code, 401)  # Bad Request

        # Check if the response contains an error message
        self.assertEqual('invalid_client', response.json()['error'])
