from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.all_products, name= 'all_products'),
    path('search/', views.search, name='search'),
    path('product_page', views.all_products_in_product_page, name='all_products_in_product_page'),
    path('addcomment/', views.addcomment, name='addcomment'),
    path('<slug:slug>', views.product_detail, name = 'product_detail'),

]
