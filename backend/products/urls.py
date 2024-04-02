from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
