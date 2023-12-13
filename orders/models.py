from decimal import Decimal
from django.conf import settings
from django.db import models
from account.models import Address
from store.models import Product
from django.utils.translation import gettext_lazy as _

choices = (('Received', 'Received'),
        ('Scheduled', 'Scheduled'), 
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        )


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=100)
    delivery_instructions = models.CharField(
        _("Delivery Instructions"), max_length=250, null = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)
    order_status = models.CharField(max_length=100, choices= choices, default="Received") 
    

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
   
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.order.id)


class ReturnPolicy(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='return_policy')
    return_reason = models.TextField(_("Return Reason"))
    return_date = models.DateTimeField(_("Return Date"), auto_now_add=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_accepted = models.BooleanField(_("Is Accepted"), default=False)

    def __str__(self):
        return str(f"Return for Order {self.order.id}")