# authapp/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from tests import User

class RegistrationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.URL = '/auth/register/'

    def test_user_registration_valid_data(self):
        data = {
            'email': 'test@example.com',
            'password': 'strongpassword123',
            'password2': 'strongpassword123',
        }

        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_user_registration_weak_password(self):
        data = {
            'email': 'test@example.com',
            'password': 'weak',
            'password2': 'weak',
        }

        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn('password', response.data)  # Check if 'password' field error is present
        self.assertIn('8 letters or more, must contains numbers', str(response.data['password'][0]))  # Check the specific error message

    def test_user_registration_passwords_not_matching(self):
        data = {
            'email': 'test@example.com',
            'password': 'strongpassword123',
            'password2': 'differentpassword',
        }

        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn('password2', response.data)  # Check if 'password2' field error is present
        self.assertIn('Passwords do not match.', str(response.data['password2'][0]))  # Check the specific error message

    # Add more tests as needed
