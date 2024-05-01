from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product

class CategoryListTest(TestCase):
    def setUp(self):
        # Create 16 categories
        number_of_categories = 16
        for category_id in range(number_of_categories):
            Category.objects.create(name=f'Test category {category_id}')

        # Get urls
        self.category = Category.objects.last()
        self.list_url = reverse('category-list')
        self.detail_url = reverse('category-detail', kwargs={'pk': self.category.id})


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

    # Test if 
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