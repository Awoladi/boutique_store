from django.urls import path
from .views import shop_view, product_list, home_view, index, cart_detail, edit_product, delete_product

app_name = 'shop'

urlpatterns = [
    path('', shop_view, name='shop_index'),  # Renamed to avoid confusion
    path('products/', product_list, name='product_list'),
    path('home/', home_view, name='home_view'),
    path('index/', index, name='index'),
    path('cart/', cart_detail, name='cart_detail'),
    path('edit/<int:product_id>/', edit_product, name='edit_product'),
    path('delete/<int:product_id>/', delete_product, name='delete_product'),
]