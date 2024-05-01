from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
import json

from django.contrib.auth.models import Group, User
from products.models import Category, Product



class CategoryViewSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create client and manager users, generate JWT tokens
        cls.client_user = User.objects.create_user(
            username='Client', 
            email='client@dev.com',
            password= make_password('client_pass')
        )
        client_group = Group.objects.get(name='client') 
        cls.client_user.groups.add(client_group)
        tkn = RefreshToken.for_user(cls.client_user).access_token
        cls.client_token = {"HTTP_AUTHORIZATION":f'Bearer {tkn}'}
        cls.manager_user = User.objects.create_user(
            username='Manager',
            email='manager@dev.com',
            password=make_password('manager_pass')
        )
        manager_group = Group.objects.get(name='manager')
        cls.manager_user.groups.add(manager_group)
        tkn = RefreshToken.for_user(cls.manager_user).access_token
        cls.manager_token = {"HTTP_AUTHORIZATION":f'Bearer {tkn}'}

        # Create 16 categories
        number_of_categories = 16
        for category_id in range(number_of_categories):
            Category.objects.create(name=f'Test category {category_id}')

        # Category URLs
        cls.category = Category.objects.last()
        cls.list_url = reverse('category-list')
        cls.detail_url = reverse('category-detail', kwargs={'pk': cls.category.id})


    # List tests
    def test_list_url_exists_at_desired_location(self):
        response = self.client.get('/products/categories/')
        self.assertEqual(response.status_code, 200)

    def test_list_url_accessible_by_name(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_list_pagination_is_ten(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 10)

    def test_lists_all_categories(self):
        response = self.client.get((self.list_url)+'?offset=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 6)

    # Detail tests
    def test_detail_url_exists_at_desired_location(self):
        response = self.client.get('/products/categories/', kwargs={'pk': self.category.id})
        self.assertEqual(response.status_code, 200)

    def test_detail_url_accessible_by_name(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.category.name)

    # Non-safe methods tests - unauthorized
    def test_category_create_not_allowed(self):
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, 401)

    def test_category_delete_not_allowed(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 401)

    def test_category_update_not_allowed(self):
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, 401)

    def test_category_partial_update_not_allowed(self):
        response = self.client.patch(self.detail_url)
        self.assertEqual(response.status_code, 401)

    # Non-safe methods tests - client forbidden
    def test_category_create_not_allowed(self):
        response = self.client.post(self.list_url, **self.client_token)
        self.assertEqual(response.status_code, 403)

    def test_category_delete_not_allowed(self):
        response = self.client.delete(self.detail_url, **self.client_token)
        self.assertEqual(response.status_code, 403)

    def test_category_update_not_allowed(self):
        response = self.client.put(self.detail_url, **self.client_token)
        self.assertEqual(response.status_code, 403)

    def test_category_partial_update_not_allowed(self):
        response = self.client.patch(self.detail_url, **self.client_token)
        self.assertEqual(response.status_code, 403)

    # Non-safe methods tests - manager
    def test_category_create_allowed(self):
        data = {"name": "manager category"}
        response = self.client.post(
            self.list_url,
            data=data,
            **self.manager_token,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], data['name'])

    def test_category_update_allowed(self):
        data = {"name": "manager category update"}
        response = self.client.put(
            self.detail_url,
            data=data,
            **self.manager_token,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], data['name'])

    def test_category_partial_update_allowed(self):
        data = {"name": "category partial update"}
        response = self.client.patch(
            self.detail_url,
            data=data,
            **self.manager_token,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], data['name'])

    def test_category_name_over_30_not_allowed(self):
        data = {"name": "over 30 characters category update"}
        response = self.client.put(
            self.detail_url,
            data=data,
            **self.manager_token,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
    
    def test_category_delete_allowed(self):
        response = self.client.delete(self.detail_url, **self.manager_token)
        self.assertEqual(response.status_code, 204)
        response = self.client.get(self.detail_url, **self.manager_token)
        self.assertEqual(response.status_code, 404)
