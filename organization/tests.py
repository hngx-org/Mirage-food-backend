from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Organization

class PersonAPITest(TestCase):
    print("=============================")
    print("This script has 5 tests and it all starts by creating an organization instance with parsed data, some correct others incorrect for testing purpose.")
    print("=============================")
    
    def setUp(self):
        self.client = APIClient()
        self.person_data = {'name': 'John Doe', 'email': 'john@example.com'}
        self.url = reverse('organization/invitations') 
    
    def test_create_person(self):
        response = self.client.post(self.url, self.person_data, format='json')
        print(f"Attempted to create an organization using valid data {response}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_person(self):
        organize  = Organization.objects.create(name='Alice', email='alice@example.com')
        response = self.client.get(reverse('users/<int:user_id>/organizations/<int:org_id>', args=[organize.id]))
        print(f"Attempted to fetch an organization with valid id  {response}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_person(self):
        organize = Organization.objects.create(name='Bob', email='bob@example.com')
        updated_data = {'name': 'Updated Bob', 'email': 'updated_bob@example.com'}
        response = self.client.put(reverse('organization/<int:pk>/', args=[organize.id]), updated_data,
        format='json')
        print(f"Attempted to update an organization with valid id {response}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_person(self):
        organize = Organization.objects.create(name='Charlie', email='charlie@example.com')
        response = self.client.delete(reverse('users/<int:org_id>/', args=[organize.id]))
        print(f"Attempted to delete an organizaton with valid ID {response}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_invalid_data(self):
        invalid_data = {'name': 123, 'email': 'invalid-email'} 
        response = self.client.post(self.url, invalid_data, format='json')
        print(f"Attempted to create an organization with invalid data  {response}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
