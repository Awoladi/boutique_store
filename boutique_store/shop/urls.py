from django.urls import path
from .views import shop_view, product_list, home_view, index, cart_detail

app_name = 'shop'

urlpatterns = [
    path('', shop_view, name='shop_index'),  # Renamed to avoid confusion
    path('products/', product_list, name='product_list'),
    path('home/', home_view, name='home_view'),
    path('index/', index, name='index'),
    path('cart/', cart_detail, name='cart_detail'),
]