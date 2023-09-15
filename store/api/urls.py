from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', views.ProductModelSetView)
router.register(r'basket', views.BasketItemModelSetView)

urlpatterns = [
    path('', include(router.urls)),
]
