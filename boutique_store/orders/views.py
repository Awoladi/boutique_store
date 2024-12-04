from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Order, OrderItem
from products.models import Product

class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
