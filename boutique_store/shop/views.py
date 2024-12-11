
# Create your views here.
from django.shortcuts import render
from .models import Product, Category

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'shop/detail.html', {'products': products, 'categories': categories})


def home_view(request):
    return render(request, 'shop/home.html')

def index(request):
    return render(request, 'shop/index.html')

def cart_detail(request):
    return render(request, 'cart/cart_detail.html', {'cart': cart})