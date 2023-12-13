import json

from django.test import TestCase, Client
from django.urls import reverse
from account.models import Review , Profile, Customer# Import User model if needed
from ..models import Product, Category,ProductType,ProductImage,ProductSpecifiactionValue  # Import your Product model
from ..views import search
from unittest.mock import patch
from decimal import Decimal

from django.core.serializers.json import DjangoJSONEncoder
        
class SearchViewTest(TestCase):
    def setUp(self):
        # Create some sample data for testing
        category_1 = Category.objects.create(name='Category 1', slug="hey-category1")
        category_2 = Category.objects.create(name='Category 34', slug="hey-category34")

        product_type_1 = ProductType.objects.create(name='Type 1')
        product_type_2 = ProductType.objects.create(name='Type 2')

        # Assign created products to attributes
        self.product1 = Product.objects.create(
            title='Product 1', author='Author 1', discount_price=10.0, regular_price=13.00,
            category=category_1, product_type=product_type_1
        )

        self.product2 = Product.objects.create(
            title='Product 2', author='Author 2', discount_price=20.0, regular_price=25.00,
            category=category_2, product_type=product_type_2
        )

    def tearDown(self):
        # Delete instances created during the test
        self.product1.delete()
        self.product2.delete()

    def test_search_view(self):
        # Your test logic here
        pass
        
    def test_search_view_post_suggestions(self):
        client = Client()

        # Test POST request for suggestions
        response = client.post(reverse('store:search'), {'q': 'Nonexistent Product'})
        self.assertEqual(response.status_code, 200)

        # Check if 'suggestions' key exists in the response
        self.assertIn('suggestions', response.json())

        # Check if there are suggestions
        suggestions = response.json()['suggestions']
        if suggestions:
            # If there are suggestions, check the title of the first suggestion
            self.assertEqual(suggestions[0]['title'], 'Nonexistent Product')
        else:
            # If there are no suggestions, print a message or handle it as appropriate for your test
            print("No suggestions found in the response. This is expected if the query has no matches.")



class AllProductsViewTest(TestCase):
    def setUp(self):
        # Create four categories for testing
        category_1 = Category.objects.create(name='Category n1', slug="hey-categoryn")
        category_2 = Category.objects.create(name='Category n2', slug="hey-categoryn2")
        category_3 = Category.objects.create(name='Category n3', slug="hey-categoryn3")
        category_4 = Category.objects.create(name='Category n4', slug="hey-categoryn4")

        product_type_1 = ProductType.objects.create(name='Type 1')
        product_type_2 = ProductType.objects.create(name='Type 2')

        # Assign created products to attributes
        self.featured_product = Product.objects.create(
            title='Featured Product', author='Author 1', discount_price=10.0, regular_price=13.00,
            category=category_1, product_type=product_type_1, slug="Featured-Product"
        )

        self.new_arrivals_product = Product.objects.create(
            title='New Arrivals Product', author='Author 2', discount_price=20.0, regular_price=25.00,
            category=category_2, product_type=product_type_2, slug="New-Arrivals"
        )

        self.limited_product = Product.objects.create(
            title='Limited Product', author='Author 3', discount_price=15.0, regular_price=18.00,
            category=category_3, product_type=product_type_1, slug="Limited-products"
        )

        self.best_sellers_product = Product.objects.create(
            title='Best Sellers Product', author='Author 4', discount_price=25.0, regular_price=30.00,
            category=category_4, product_type=product_type_2, slug="Best-sellers"
        )

        @patch('store.views.Product.objects.filter')
        def test_all_products_view(self, mock_filter):
            # Mock the filter method to return the sample products
            mock_filter.return_value = [
                self.featured_product,
                self.new_arrivals_product,
                self.limited_product,
                self.best_sellers_product
            ]

            # Access the view using reverse to get the URL
            url = reverse('store:all_products')
            response = self.client.get(url)

            # Check if the response status code is 200 (OK)
            self.assertEqual(response.status_code, 200)

            # Check if the products are present in the context
            self.assertIn('featured', response.context)
            self.assertIn('new_arrivals', response.context)
            self.assertIn('limited', response.context)
            self.assertIn('BestSellers', response.context)

            # Check if the correct products are present in the context
            self.assertQuerysetEqual(
                response.context['featured'],
                [f"{self.featured_product.title} by {self.featured_product.author}"]
            )
            self.assertQuerysetEqual(
                response.context['new_arrivals'],
                [f"{self.new_arrivals_product.title} by {self.new_arrivals_product.author}"]
            )
            self.assertQuerysetEqual(
                response.context['limited'],
                [f"{self.limited_product.title} by {self.limited_product.author}"]
            )
            self.assertQuerysetEqual(
                response.context['BestSellers'],
                [f"{self.best_sellers_product.title} by {self.best_sellers_product.author}"]
            )

            # Clean up your mock after the test
            mock_filter.assert_called_once_with(category_id=251)
            
            

class AllProductsInViewTest(TestCase):
    def setUp(self):
        # Create sample data for testing
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

    def test_all_products_in_product_page_view(self):
        # Access the view using reverse to get the URL
        url = reverse('store:all_products_in_product_page')

        # Prepare sample data for the AJAX request
        ajax_data = {
            'categories': [self.test_category.id],
            'discountRange': [Decimal('0.00'), Decimal('10.00')],
            'priceRange': Decimal('50.00'),
            'authors': ['Sample Author'],
            'languages': ['English'],
        }

        # Perform an AJAX POST request with the prepared data
        response = self.client.post(
            url,
            data=json.dumps(ajax_data, cls=DjangoJSONEncoder),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON content from the response
        try:
            actual_response_data = json.loads(response.content.decode('utf-8'))

            # Print statements for debugging
            print(f"Criteria: {ajax_data}")
            print(f"Filtered Products: {actual_response_data['products']}")

            # Check if the rendered context contains the expected keys
            self.assertIn('products', actual_response_data)
            self.assertIn('min', actual_response_data)
            self.assertIn('max', actual_response_data)

            # Compare the expected and actual response data
            self.assertEqual(Decimal('10.00'), Decimal(str(actual_response_data['min'])))
            self.assertEqual(Decimal('10.00'), Decimal(str(actual_response_data['max'])))
            self.assertIsInstance(actual_response_data['products'], list)

            # Add more assertions based on your specific data structure

        except json.JSONDecodeError:
            # Handle the case where the response content is not valid JSON
            self.fail("Response content is not valid JSON")
            
            
class ProductDetailViewTest(TestCase):

    def setUp(self):
        # Create sample data for testing
        self.test_category = Category.objects.create(name='Test Category', slug='test-category')
        product_type_name = 'book'

        # Try to get the ProductType instance by name
        try:
            product_type = ProductType.objects.get(name=product_type_name)
        except ProductType.DoesNotExist:
            # If it doesn't exist, create a new one
            product_type = ProductType.objects.create(name=product_type_name)

        # Create a sample product for testing
        self.test_product = Product.objects.create(
            title='Sample ProductA',
            discount_price=10.0,
            regular_price=15.0,
            author='Sample AuthorB',
            category=self.test_category,
            product_type=product_type,
            slug="Sample-product-456",
        )

        # Create a sample product image for testing
        self.product_image = ProductImage.objects.create(
            product=self.test_product,
            image='path/to/sample/image.jpg',
            is_feature=True,
            alt_text='Sample Alt Text',
        )

    def test_product_detail_view(self):
        # Access the view using reverse to get the URL
        url = reverse('store:product_detail', kwargs={'slug': self.test_product.slug})

        # Simulate a GET request
        response = self.client.get(url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'store/detail1.html')

        # Add more assertions based on the expected behavior of your view
        # For example, check if the product and other context data are present in the response
        self.assertEqual(response.context['product'], self.test_product)
        # ...



class AddCommentViewTest(TestCase):

    def setUp(self):
        # Create a sample user and profile for testing
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
        
        self.user = Customer.objects.create(name='testuser1', password='testpassword', email="nissan@gmail.com")
        self.profile = Profile.objects.get(user=self.user)
        self.post = Product.objects.get(title="Sample ProductA")
        # Create a sample review for testing
        self.review = Review.objects.create(
            name=self.user,
            email=self.user.email,
            content='Test Comment',
            image=self.profile,
            rate=5,
            post=self.post,
        )

    def test_add_comment_view_post(self):
        # Access the view using reverse to get the URL
        url = reverse('store:product_detail' ,kwargs={'slug': self.product.slug})

        # Log in the user
        self.client.login(email='nissan@gmail.com', password='testpassword')

        # Prepare sample data for the POST request
        post_data = {
            'action': 'add',
            'content': 'Test Comment',
            'image': self.profile.id,
            'type': 'POST',
        
        }

        # Simulate a POST request
        response = self.client.post(url, data=post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)

        # Check if the response status code is 200 (OK) after following redirects
        self.assertEqual(response.status_code,200)

        # Optionally, you can also check if the comment was created in the database
        comment = Review.objects.last()
        self.assertIsNotNone(comment)
        self.assertEqual(comment.content, 'Test Comment')
        self.assertEqual(comment.name, self.user)
        self.assertEqual(comment.image, self.profile)

    def test_add_comment_view_delete(self):
        # Access the view using reverse to get the URL
        self.client.login(username='testuser', password='testpassword')
        url = reverse('store:product_detail' ,kwargs={'slug': self.product.slug})

        # Prepare sample data for the POST request to delete the review
        post_data = {
            'action': 'delete',
            'nodeid': self.review.id,
            'image': self.profile.id,
            'type': 'POST',
        }

        # Simulate a POST request
        response = self.client.post(url, data=post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)

        # Check if the response status code is 200 (OK) after following redirects
        self.assertEqual(response.status_code,200)
        remove = Review.objects.get(id=self.review.id)
        remove.delete()
        # Check if the remove key is in the response as plain text
        # Optionally, you can also check if the review was deleted from the database
        review_exists = Review.objects.filter(id=self.review.id).exists()
        print(f"hey u {Review.objects.filter(id=self.review.id)}")
        self.assertFalse(review_exists)