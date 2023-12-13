
from django.db import models
from orders.models import Order, OrderItem
from django.utils.translation import gettext_lazy as _
from store.models import ProductImage
from django.urls import reverse
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey

choices = (('published', 'published'),
           ('Sold', 'Sold'),
           )


class Category(MPTTModel):
    """
    Category Table Implementation with MPTT
    """
    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=520,
        unique=True,    
    )
    slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=520, unique=True )
    parent = TreeForeignKey("self", on_delete = models.CASCADE, null = True, blank = True,related_name = "children")
    is_active = models.BooleanField(default= True)
    
    class MPTTMeta:
        order_insertion_by = ["name"]
        
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        
    def get_absolute_url(self):
        return reverse("sellbook:category_list", args=[self.slug])
    
    def __str__(self):
        return self.name
    


class sell_old_books(models.Model):
    user_id = models.IntegerField()
    selling_prod = models.ForeignKey(
        OrderItem, on_delete=models.CASCADE, related_name='items')
    selling_user = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_user')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    description = models.TextField(verbose_name=_(
        "description"), help_text=_("Not Required"), blank=True)
    slug = models.SlugField(max_length=520)
    title = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=520, null=True)
    regular_price = models.DecimalField(
        verbose_name=_("Regular Price"),
        help_text=_("Maximum 9999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 9999.99"),
            },
        },
        max_digits=6,
        decimal_places=2,
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount price"),
        help_text=_("Maximum 9999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 9999.99"),
            },
        },
        max_digits=6,
        decimal_places=2,
    )
    discount_percentage = models.DecimalField(
        verbose_name=_("Discount percentage"),
        help_text=_("100%"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 100% just type the number of percent "),
            },
        },
        max_digits=5,
        decimal_places=2,
    )
    image1 = models.ImageField(
        verbose_name=_("image1"),
        help_text=_("Upload a product image"),
        upload_to="old_books/",
        default="old_books/default.png",
    )
    image2 = models.ImageField(
        verbose_name=_("image2"),
        help_text=_("Upload a product image"),
        upload_to="old_books/",
        default="old_books/default.png",
    )
    image3 = models.ImageField(
        verbose_name=_("image3"),
        help_text=_("Upload a product image"),
        upload_to="old_books/",
        default="old_books/default.png",
    )
    created_at = models.DateTimeField(
        _("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    real_quantity = models.IntegerField(default=1)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=100, choices=choices, default="published")

    def get_absolute_url(self):
        return reverse("sellbook:product_detail", args=[self.slug])

    def get_absolute_url_prod(self):
        return reverse("sellbook:product_detail1", args=[self.slug])
    
    def __str__(self):
        return str(self.selling_prod.product)


