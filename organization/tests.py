from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
# from django.contrib.auth.models import User
from users.models import User
from .models import Organization, OrganizationLunchWallet, OrganizationInvites
from decimal import Decimal


# Create your tests here.
class TestCreateOrganization(APITestCase):
  """Test for creating an Organization"""
  
  def setUp(self):
    self.client = APIClient()
    self.url = "/api/organization/create"
    self.data = {
      "name": "Mirage",
      "lunch_price": Decimal("10.00"),
      "currency": "NAIRA"
    }
    self.bad_data = {}

  def test_if_user_is_anonymous_returns_401(self):
    self.client = APIClient()
    response = self.client.post(self.url, self.data)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
  
  def test_if_user_authenticated_and_correct_data_returns_201(self):
    user = User.objects.create_user(
            email="testuser@example.com",
            password="password",
            first_name="John",
            last_name="Doe",
            profile_pic="cloudinary_url",
            phone="1234567890",
            refresh_token="your_refresh_token",
            bank_number="your_bank_number",
            bank_code="your_bank_code",
            bank_name="your_bank_name",
            lunch_credit_balance="100.00",
          )
    # user.is_staff = True
    # user.is_superuser = True
    user.save()
    
    self.client.login(email="user@gmail.com", password="password")
    response = self.client.post(self.url, self.data)  
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Organization.objects.count(), 1)
  
  def test_if_user_authenticated_and_not_correct_data_returns_400(self):
    user = User.objects.create_user(
            email="user@gmail.com",
            password="password"
          )
    user.save()
    
    self.client.login(email="user@gmail.com", password="password")
    
    response = self.client.post(self.url, self.bad_data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)