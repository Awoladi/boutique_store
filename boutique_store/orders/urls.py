from django.urls import path
from .views import checkout, order_list

app_name = 'orders'

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('my-orders/', order_list, name='order_list'),
]
