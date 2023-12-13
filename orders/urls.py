from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.add, name='add'),
    path('return_book/<int:order_id>/', views.return_book, name='return_book'),
    path('return_book_submit/<int:order_id>/', views.return_book_submit, name='return_book_submit'),
]
