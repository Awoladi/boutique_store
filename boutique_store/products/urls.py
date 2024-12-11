from django.urls import path
from .views import ProductListView, ProductDetailView

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),  # List view
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # Detail view
]
