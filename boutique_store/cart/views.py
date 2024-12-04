from django.shortcuts import render, redirect
from django.views import View
from .models import CartItem
from products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin

class CartDetailView(View):
    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        return render(request, 'cart_detail.html', {'cart_items': cart_items})

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart:cart_detail')


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.filter(user=request.user, product=product).first()
        if cart_item:
            cart_item.delete()
        return redirect('cart:cart_detail')
