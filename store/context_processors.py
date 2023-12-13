from .models import Category
from django.shortcuts import get_object_or_404, render



def categories(request):
    return {
        'categories': Category.objects.all()
    }


