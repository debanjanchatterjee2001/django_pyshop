from django.urls import path
from . import views
import accounts

urlpatterns = [
    path('', views.cart, name='cart'),
    path('confirm/', views.cart_confirm),
    path('delete/', views.delete_item),
    path('confirm/login', accounts.views.login),
]
