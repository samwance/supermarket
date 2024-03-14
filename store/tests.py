from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from store.models import Category, SubCategory, Product, CartProduct, Cart
from store.serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, CartProductSerializer, CartSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class CategoryTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_category_list(self):
        response = self.client.get(reverse('store:cat_list'))
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], categories.count())


class SubCategoryTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.sub_category = SubCategory.objects.create(name='Test SubCategory', slug='test-subcategory', parent_category=self.category)
        self.client = APIClient()

    def test_get_sub_category_list(self):
        response = self.client.get(reverse('store:sub_cat_list', kwargs={'cat': self.category.slug}))
        sub_categories = SubCategory.objects.filter(parent_category=self.category)
        serializer = SubCategorySerializer(sub_categories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], sub_categories.count())


class ProductTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.sub_category = SubCategory.objects.create(name='Test SubCategory', slug='test-subcategory', parent_category=self.category)
        self.product = Product.objects.create(name='Test Product', slug='test-product', category=self.category, subcategory=self.sub_category, price=19.00)
        self.client = APIClient()

    def test_get_product_list(self):
        response = self.client.get(reverse('store:product_list'))
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], len(serializer.data))
        for product, serialized_product in zip(products, serializer.data):
            self.assertEqual(product.id, serialized_product['id'])
            self.assertEqual(product.name, serialized_product['name'])
            self.assertEqual(Decimal(serialized_product['price']), product.price)
            self.assertEqual(product.category.id, serialized_product['category'])
            self.assertEqual(product.category.name, self.category.name)
            self.assertEqual(product.subcategory.id, serialized_product['subcategory'])
            self.assertEqual(product.subcategory.name, self.sub_category.name)