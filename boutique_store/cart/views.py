from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import CartItem
from products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin


class CartDetailView(LoginRequiredMixin, View):
    """Displays the cart for the logged-in user"""

    def get(self, request):
        # Ensure only logged-in users can view the cart
        if not request.user.is_authenticated:
            return redirect('users:login')  # Redirect to login page if not authenticated

        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'cart/cart_detail.html', {
            'cart_items': cart_items,
            'total_price': total_price
        })


class AddToCartView(LoginRequiredMixin, View):
    """Adds a product to the user's cart"""

    def post(self, request, product_id):
        # Ensure the product exists before adding to cart
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart:cart_detail')


class RemoveFromCartView(LoginRequiredMixin, View):
    """Removes a product from the user's cart"""

    def post(self, request, product_id):
        # Ensure the product exists before removing from cart
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.filter(user=request.user, product=product).first()
        if cart_item:
            cart_item.delete()
        return redirect('cart:cart_detail')
