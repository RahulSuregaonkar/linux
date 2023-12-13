from account.models import Customer
from django.test import TestCase
from django.urls import reverse
from django.test import TestCase, Client
from account.models import Customer,Address
from django.urls import reverse
from store.models import Product,Category,ProductImage,ProductType 
import json
from ..models import Save_For_Later

class TestBasketView(TestCase):
    def setUp(self):
        self.user = Customer.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='testpassword'
        )
        self.client = Client()
                # Create a user for testing
        self.test_category = Category.objects.create(name='Test Category', slug='test-category')
        product_type_name = 'book'

        # Try to get the ProductType instance by name
        try:
            product_type = ProductType.objects.get(name=product_type_name)
        except ProductType.DoesNotExist:
            # If it doesn't exist, create a new one
            product_type = ProductType.objects.create(name=product_type_name)
        self.product = Product.objects.create(
            title='Sample ProductA',
            discount_price=10.0,
            regular_price=15.0,
            author='Sample AuthorB',
            category=self.test_category,
            product_type=product_type,
            slug="Sample-product-456",
        )
        self.product_image = ProductImage.objects.create(
            product=self.product,
            image='path/to/sample/image.jpg',
            is_feature=True,
            alt_text='Sample Alt Text',
        )
        self.post = Product.objects.get(title="Sample ProductA")
        self.client.post(
            reverse('basket:basket_add'), {"productid": 1, "productqty": 1, "action": "post"}, xhr=True)
        self.client.post(
            reverse('basket:basket_add'), {"productid": 2, "productqty": 2, "action": "post"}, xhr=True)

    def test_basket_url(self):
        """
        Test homepage response status
        """
        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 302)

    def test_basket_summary_view(self):
        url = reverse('basket:basket_summary')  # Assuming you have a name for the URL pattern
        response = self.client.get(url)
        self.assertEqual(response.status_code,302)


    def test_basket_add_view(self):
        url = reverse('basket:basket_add')  
        response = self.client.post(url, {'action': 'post', 'productid': self.product.id, 'productqty': 2})
        self.assertEqual(response.status_code, 302)


    def test_basket_delete_view(self):
        url = reverse('basket:basket_delete')  
        response = self.client.post(url, {'action': 'post', 'productid': self.product.id})
        self.assertEqual(response.status_code, 302)


    def test_basket_update_view(self):
        url = reverse('basket:basket_update') 
        response = self.client.post(url, {'action': 'post', 'productid': self.product.id, 'productqty': 3})
        self.assertEqual(response.status_code, 302)


    def test_add_to_save_for_later_view(self):
        url = reverse('basket:add_to_save_for_later', args=[self.product.id])
        response = self.client.get(url, {'quantity': 1})
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_remove_save_for_later_view(self):
        saved_item = Save_For_Later.objects.create(product=self.product, user=self.user, quantity=1)
        url = reverse('basket:remove_save_for_later', args=[saved_item.id, self.product.id])
        response = self.client.get(url, {'quantity': 1})
        self.assertEqual(response.status_code, 302)
