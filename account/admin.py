from django.contrib import admin

from .models import Customer, Profile, Address, Review
from mptt.admin import MPTTModelAdmin

admin.site.register(Customer)

admin.site.register(Profile)

admin.site.register(Address)

admin.site.register(Review, MPTTModelAdmin)