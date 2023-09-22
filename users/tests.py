from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('api/auth/user/signup/')  # Adjust the URL name as per your project

    def test_user_registration(self):
        data = {
            "email": "user@example.com",
            "password": "password123",
            "first_name": "",
            "last_name": "",
            "phone_number": ""
        }

        response = self.client.post(self.registration_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that a user with the provided email exists in the database
        user = User.objects.get(email=data['email'])
        self.assertEqual(user.email, data['email'])

    def test_user_registration_with_missing_fields(self):
        # Test registration with missing fields (should return 400 Bad Request)
        data = {
            "email": "user@example.com",
            "password": "password123",
            # Other fields are missing
        }

        response = self.client.post(self.registration_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_with_existing_email(self):
        # Create a user with the same email as in the test data
        User.objects.create_user(
            email="user@example.com",
            password="existing_password"
        )

        # Test registration with an email that already exists (should return 400 Bad Request)
        data = {
            "email": "user@example.com",
            "password": "password123",
            "first_name": "",
            "last_name": "",
            "phone_number": ""
        }

        response = self.client.post(self.registration_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

