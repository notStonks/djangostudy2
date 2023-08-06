from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    # path('products/page/<int:page_number>', views.products, name='paginator'),
    path('products/category/<int:category_id>', views.products, name='category'),
    path('item/add/<int:product_id>', views.item_add, name='item_add'),
    path('item/remove/<int:basket_id>', views.item_remove, name='item_remove'),

]
