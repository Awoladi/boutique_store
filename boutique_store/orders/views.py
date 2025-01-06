from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem
from django.views.generic import ListView, DetailView
from .models import Order, OrderItem
from products.models import Product

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('cart:cart_detail')  # Redirect to cart if empty

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Create an order and order items
    order = Order.objects.create(user=request.user, total_price=total_price)
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price * item.quantity
        )
    cart_items.delete()  # Clear the cart
    return render(request, 'orders/checkout_success.html', {'order': order})

class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})