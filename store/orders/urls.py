from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='orders'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('success/', views.SuccessTemplateView.as_view(), name='success'),
    path('cancel/', views.CancelTemplateView.as_view(), name='cancel'),
    path('webhook/', views.stripe_webhook_view, name='webhook'),
]
