from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartDetailView, name='cart'),
    path('add/<int:product_id>/', views.AddToCartView, name='add_to_cart'),
]
