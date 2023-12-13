from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Customer, Profile, Address, Review,user_directory_path,CustomAccountManager
from store.models import Product,ProductImage,ProductType,Category

class ModelTestCase(TestCase):

    def setUp(self):
            self.user = Customer.objects.create_user(
                email='testuser@example.com',
                name='Test User',
                password='testpassword'
            )
            self.client = Client()

            # Additional setup for testing
            self.test_category = Category.objects.create(name='Test Category', slug='test-category')
            product_type_name = 'book'

            try:
                product_type = ProductType.objects.get(name=product_type_name)
            except ProductType.DoesNotExist:
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
            
    def test_customer_model(self):
        customer = Customer.objects.create(
            email='customer@example.com',
            name='Customer Name',
            mobile='123456789',
            country='US',
            is_active=True,
            is_staff=True
        )
        self.assertEqual(str(customer), 'Customer Name')
        self.assertTrue(customer.is_active)
        self.assertTrue(customer.is_staff)

    def test_profile_model(self):
        profile = Profile.objects.get(
            user=self.user
        )
        self.assertEqual(str(profile), 'Test User')

    def test_address_model(self):
        address = Address.objects.create(
            customer=self.user,
            full_name='John Doe',
            phone='123456789',
            postcode='12345',
            address_line='123 Main St',
            address_line2='Apt 1',
            town_city='City',
            delivery_instructions='Leave at the door',
            default=True
        )
        self.assertEqual(str(address), 'Test User')

    def test_review_model(self):
        review = Review.objects.create(
            post=self.post,  # Replace with a valid Product instance
            name=self.user,
            email='test@example.com',
            content='Test Review',
            rate=4,
            image=Profile.objects.get(user=self.user)
        )
        self.assertEqual(str(review), 'Test User')
        self.assertEqual(review.rate, 4)
        

class CustomAccountManagerTests(TestCase):

    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'password123',
            'is_active':True,
        }

    def test_create_user(self):
        User = get_user_model()
        manager = User.objects
        user = manager.create_user(**self.user_data)

        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.name, self.user_data['name'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active) 

    def test_create_superuser(self):
        User = get_user_model()
        manager = User.objects
        superuser_data = {
            'email': 'admin@example.com',
            'name': 'Admin User',
            'password': 'adminpassword123',
            'is_staff': True,
            'is_superuser': True,
        }
        superuser = manager.create_superuser(**superuser_data)

        self.assertEqual(superuser.email, superuser_data['email'])
        self.assertEqual(superuser.name, superuser_data['name'])
        self.assertTrue(superuser.check_password(superuser_data['password']))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

def test_create_superuser_without_staff(self):
    User = get_user_model()
    manager = User.objects
    superuser_data = {
        'email': 'admin@example.com',
        'name': 'Admin User',
        'password': 'adminpassword123',
        'is_superuser': True,
    }

    with self.assertRaises(ValueError):
        manager.create_superuser(**superuser_data)

def test_create_superuser_without_superuser(self):
    User = get_user_model()
    manager = User.objects
    superuser_data = {
        'email': 'admin@example.com',
        'name': 'Admin User',
        'password': 'adminpassword123',
        'is_staff': True,
    }

    with self.assertRaises(ValueError):
        manager.create_superuser(**superuser_data)

def test_create_user(self):
    User = get_user_model()
    manager = User.objects
    user = manager.create_user(**self.user_data)

    self.assertEqual(user.email, self.user_data['email'])
    self.assertEqual(user.name, self.user_data['name'])
    self.assertTrue(user.check_password(self.user_data['password']))
    self.assertFalse(user.is_staff)
    self.assertFalse(user.is_superuser)
    self.assertTrue(user.is_active)