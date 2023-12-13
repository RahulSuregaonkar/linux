from django.urls import path

from . import views

app_name = 'sellbook'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('sellbook/<slug:category_slug>/', views.category_list, name='category_list'),
    path('sellbook/<slug:slug>', views.product_detail, name='product_detail'),
    path('sellbook1/<slug:slug>', views.product_detail1, name='product_detail1'),
    path('mybooks/', views.mybooks, name='mybooks'),
    path('mybooks/edit/<int:pk>', views.edit_books, name='edit_books'),
    path('mybooks/delete/<int:pk>', views.delete_books, name='delete_books'),
    path('mybooks/sold_books/', views.mysoldbooks, name='mysoldbooks'),
]
