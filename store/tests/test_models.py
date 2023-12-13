from account.models import Customer
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
import uuid
from django.db.utils import IntegrityError

from store.models import Category, Product, ProductImage, ProductSpecifiactionValue,ProductSpecification,ProductType



class CategoryModelTest(TestCase):
    def generate_unique_name(self):
        return f"Test Category {uuid.uuid4().hex[:6]}"

    def generate_unique_slug(self):
        return f"test-category-{uuid.uuid4().hex[:6]}"

    def setUp(self):
        # Create a sample category for testing
        self.category = Category.objects.create(
            name=self.generate_unique_name(),
            slug=self.generate_unique_slug(),
            is_active=True,
        )

    def test_category_str(self):
        # Test the __str__ method of the Category model
        self.assertEqual(str(self.category), self.category.name)

    def test_category_creation(self):
        # Test if the category is created successfully
        self.assertEqual(Category.objects.count(), 1)

    def test_unique_slug(self):
        # Test if the slug is unique
        duplicate_category = Category(
            name=self.generate_unique_name(),
            slug=self.category.slug,  # Should be the same as the first category
            is_active=True,
        )
        with self.assertRaises(Exception):
            duplicate_category.save()

    def test_tree_structure(self):
        # Test the tree structure using MPTT
        child_category = Category.objects.create(
            name=self.generate_unique_name(),
            slug=self.generate_unique_slug(),
            parent=self.category,
            is_active=True,
        )
        self.assertEqual(self.category.get_children().count(), 1)
        self.assertEqual(child_category.parent, self.category)

    def test_verbose_name_plural(self):
        # Test the plural verbose name of the model
        self.assertEqual(str(Category._meta.verbose_name_plural), "Categories")
        

class ProductModelTest(TestCase):
    def setUp(self):
        # Create a sample category for testing
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category",
            is_active=True,
        )

        # Create a sample product type for testing
        self.product_type = ProductType.objects.create(
            name="Test Product Type",
            is_active=True,
        )

        # Create a sample user for testing
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            name="Test User",
        )

        # Create a sample product for testing
        self.product = Product.objects.create(
            product_type=self.product_type,
            category=self.category,
            title="Test Product",
            author="Test Author",
            language="English",
            description="Test Description",
            slug="test-product",
            regular_price=50.0,
            discount_price=40.0,
            is_active=True,
        )

        # Create a sample product specification for testing
        self.product_specification = ProductSpecification.objects.create(
            product_type=self.product_type,
            name="Test Specification",
        )

        # Create a sample product specification value for testing
        self.product_specification_value = ProductSpecifiactionValue.objects.create(
            product=self.product,
            specification=self.product_specification,
            value="Test Value",
        )

        # Create a sample product image for testing
        image_content = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg",
        )
        self.product_image = ProductImage.objects.create(
            product=self.product,
            image=image_content,
            alt_text="Test Alt Text",
            is_feature=True,
        )

    def test_product_type_creation(self):
        self.assertEqual(ProductType.objects.count(), 1)

    def test_product_specification_creation(self):
        self.assertEqual(ProductSpecification.objects.count(), 1)

    def test_category_creation(self):
        self.assertEqual(Category.objects.count(), 1)

    def test_product_creation(self):
        self.assertEqual(Product.objects.count(), 1)

    def test_product_specification_value_creation(self):
        self.assertEqual(ProductSpecifiactionValue.objects.count(), 1)

    def test_product_image_creation(self):
        self.assertEqual(ProductImage.objects.count(), 1)

    def test_product_str_representation(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_product_specification_str_representation(self):
        self.assertEqual(str(self.product_specification), "Test Specification")

    def test_category_str_representation(self):
        self.assertEqual(str(self.category), "Test Category")

    def test_product_image_str_representation(self):
        self.assertEqual(str(self.product_image), "Test Product")
    
    def test_foreign_key_constraints(self):
        # Try to create a ProductType or get an existing one with a unique name
        product_type_name = "Test Product Type"
        try:
            product_type, created = ProductType.objects.get_or_create(name=product_type_name)
        except IntegrityError:
            # If there is an integrity error, it means the product type already exists
            product_type = ProductType.objects.get(name=product_type_name)

        # Try to create a Category or get an existing one with a unique name
        category_name = "Test Category"
        try:
            category, created = Category.objects.get_or_create(name=category_name)
        except IntegrityError:
            # If there is an integrity error, it means the category already exists
            category = Category.objects.get(name=category_name)

        # Create a product with the retrieved or created product_type and category
        product = Product.objects.create(
            title="Test Product",
            product_type=product_type,
            regular_price=10.00,
            discount_price=8.00,
            category=category,  # Provide a valid category object
        )

        # Create a product specification linked to the product_type
        product_specification = ProductSpecification.objects.create(product_type=product_type)

        # Create a product image linked to the created product
        product_image = ProductImage.objects.create(product=product)

        print("Number of Product objects before assertion:", Product.objects.count())
        # Now, you can perform assertions and additional test logic based on your models
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(ProductSpecification.objects.count(), 2)
        self.assertEqual(ProductImage.objects.count(), 2)

        # Example: Check if the product type is correctly linked to the product
        self.assertEqual(product.product_type, product_type)
        
    def tearDown(self):
        # Clean up by deleting instances created during the test
        ProductImage.objects.all().delete()
        ProductSpecifiactionValue.objects.all().delete()
        Product.objects.all().delete()
        ProductSpecification.objects.all().delete()
        Category.objects.all().delete()
        get_user_model().objects.all().delete()
        ProductType.objects.all().delete()
        
        
        