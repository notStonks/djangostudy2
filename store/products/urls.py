from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('item/add/<int:product_id>', views.item_add, name='item_add'),
    path('item/remove/<int:basket_id>', views.item_remove, name='item_remove'),

]