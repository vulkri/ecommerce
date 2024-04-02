from django.contrib import admin
from django.urls import path
from django.conf.urls import include


from . import views

urlpatterns = [
    path('create/', views.CreateOrderAPIView.as_view(), name='create-order'),
    path('top-sellers/', views.TopSellersListAPIView.as_view(), name='top-sellers'),
    path('force-remainder/', views.ForceRemainderAPIView.as_view(), name='force-remainder'),
    
]
