from django.contrib import admin

# Register your models here.
from . import models 


admin.site.register(models.Category)



@admin.register(models.sell_old_books)
class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('selling_prod','selling_user','category','description'),}
    
    
