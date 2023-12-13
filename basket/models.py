from django.db import models
from django.conf import settings
from django.urls import reverse
from store.models import Product
from account.models import Customer




class Save_For_Later(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="save_for_later_product")
    user = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name="user")
    quantity = models.IntegerField(default=1)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    def remove(self):
        self.delete()