from django.urls import path

from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.basket_summary, name='basket_summary'),
    path('add/', views.basket_add, name='basket_add'),
    path('delete/', views.basket_delete, name='basket_delete'),
    path('update/', views.basket_update, name='basket_update'),
    path('save_for_later/add_to_save_for_later/<int:id>',views.add_to_save_for_later, name='add_to_save_for_later'),
    path('save_for_later/remove_save_for_later/<int:id>/<int:id2>/',views.remove_save_for_later, name='remove_save_for_later'),
]
