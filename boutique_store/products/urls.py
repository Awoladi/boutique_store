from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    submit_review,
    category_products,
    CategoryListView,
    product_create,
    product_edit,
    product_delete,
    category_list,
    category_create,
    category_edit,
    category_delete,
)

app_name = 'products'

urlpatterns = [
    # Product-related routes
    path('', ProductListView.as_view(), name='product_list'),  # Product list view
    path('category/<slug:slug>/', ProductListView.as_view(), name='category_products'),
    path('categories/', CategoryListView.as_view(), name='category_list'),  # Category list page# Category filter view
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # Product detail view
    path('<int:pk>/submit_review/', submit_review, name='submit_review'),
    path('create/', product_create, name='product_create'),  # Product creation
    path('<int:pk>/edit/', product_edit, name='product_edit'),  # Product editing
    path('<int:pk>/delete/', product_delete, name='product_delete'),  # Product deletion

    # Category-related routes
    path('category/<slug:slug>/', category_products, name='category_products'),  # Filter by category
    path('categories/', category_list, name='category_list'),  # List all categories
    path('categories/create/', category_create, name='category_create'),  # Create category
    path('categories/<int:pk>/edit/', category_edit, name='category_edit'),  # Edit category
    path('categories/<int:pk>/delete/', category_delete, name='category_delete'),  # Delete category
]
