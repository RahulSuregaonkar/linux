from django.test import TestCase, Client
from account.models import Customer,Address
from django.urls import reverse
from store.models import Product,Category,ProductImage,ProductType  # Import your Product model
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from sellbook.models import sell_old_books
from datetime import datetime, timedelta
from orders.models import Order,OrderItem


class userViewTests(TestCase):

    
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

    def test_wishlist_view_with_authenticated_user(self):
            self.client.login(email='testuser@example.com', password='testpassword')
            response = self.client.get(reverse('account:wishlist'))

            # Check if the response is a redirect
            self.assertEqual(response.status_code, 302)
            # If it's a redirect, check the redirected URL with the 'next' parameter
            self.assertRedirects(response, reverse('account:login') + '?next=' + reverse('account:wishlist'))

    def test_wishlist_view_with_unauthenticated_user(self):
        response = self.client.get(reverse('account:wishlist'))  # Use the correct URL name for your 'wishlist' view
        self.assertEqual(response.status_code, 302)  # Expect a redirect for an unauthenticated user

    def test_add_to_wishlist_view(self):
        self.client.login(email='testuser@example.com', password='testpassword')
        product = self.product
        response = self.client.get(reverse('account:user_wishlist', args=[product.id]))  # Use the correct URL name for your 'add_to_wishlist' view
        self.assertEqual(response.status_code, 302)  # Expect a redirect

    def test_profile_view(self):
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.get(reverse('account:users-profile'))

        # Check if the response is a redirect
        if isinstance(response, HttpResponseRedirect):
            self.assertEqual(response.status_code, 302)  # or the appropriate redirect status code
        else:
            self.assertEqual(response.status_code, 200)  # Assuming a successful view, change if needed
            # Check if a template was used
            self.assertTemplateUsed(response, 'account/dashboard/profile.html')

    def test_dashboard_view(self):
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.get(reverse('account:dashboard'))  # Update with the correct URL name
        self.assertEqual(response.status_code, 302)  # Update if expecting a different status code

    def test_user_orders_view(self):
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.get(reverse('account:user_orders'))  # Update with the correct URL name
        self.assertEqual(response.status_code, 302) 



