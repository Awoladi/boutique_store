# Import Django built-in functions and classes
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views  # Import views correctly
# Import views from each app
from products.views import ProductListView, ProductDetailView
from cart.views import CartDetailView, AddToCartView, RemoveFromCartView
from users.views import login_view, logout_view, register_view
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

# Custom error handlers
handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'

from django.shortcuts import render

def home_view(request):
    return render(request, 'core/base.html')


app_name = 'core'  # Ensure namespace is defined once here only.

# Define urlpatterns
urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('', include('core.urls', namespace='core')),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls', namespace='products')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('users/', include('users.urls', namespace='users')),
    path('products/', include('shop.urls', namespace='shop')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
