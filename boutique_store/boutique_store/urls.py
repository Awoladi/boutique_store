# Import Django built-in functions and classes
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Import views from each app
from products.views import ProductListView, ProductDetailView
from cart.views import CartDetailView, AddToCartView, RemoveFromCartView
from users.views import login_view, logout_view, register_view

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'

def home(request):
    return HttpResponse("Awolfy!")

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('users/', include('users.urls', namespace='users')),
    path('', home, name='home'),
    path('', include('core.urls', namespace='core')),
    path('shop/', include('shop.urls', namespace='shop')),
]
