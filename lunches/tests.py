from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Lunch

class PersonAPITest(TestCase):
    print("=============================")
    print("This script has 5 tests and it all starts by creating a Lunch instance with parsed data, some correct others incorrect for testing purpose.")
    print("=============================")
    
    def setUp(self):
        self.client = APIClient()
        self.person_data = {'name': 'John Doe', 'email': 'john@example.com'}
        self.url = reverse('lunch/all') 
    
    def test_create_person(self):
        response = self.client.post(self.url, self.person_data, format='json')
        print(f"Attempted to create a lunch using valid data {response}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_person(self):
        lunch  = Lunch.objects.create(name='Alice', email='alice@example.com')
        response = self.client.get(reverse('lunch/<int:id>', args=[lunch.id]))
        print(f"Attempted to fetch a lunch with valid id  {response}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_person(self):
        lunch = Lunch.objects.create(name='Bob', email='bob@example.com')
        updated_data = {'name': 'Updated Bob', 'email': 'updated_bob@example.com'}
        response = self.client.put(reverse('update_lunch/<int:id>', args=[lunch.id]), updated_data,
        format='json')
        print(f"Attempted to update a lunch with valid id {response}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_person(self):
        lunch = Lunch.objects.create(name='Charlie', email='charlie@example.com')
        response = self.client.delete(reverse('lunch/<int:id>', args=[lunch.id]))
        print(f"Attempted to delete a lunch with valid ID {response}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_invalid_data(self):
        invalid_data = {'name': 123, 'email': 'invalid-email'} 
        response = self.client.post(self.url, invalid_data, format='json')
        print(f"Attempted to create lunch with invalid data  {response}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
