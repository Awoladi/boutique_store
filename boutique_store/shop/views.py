
# Create your views here.
from django.shortcuts import render
from .models import Product, Category  # Import models defined in shop/models.py

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'shop/product_list.html', {'products': products, 'categories': categories})


def home_view(request):
    return render(request, 'shop/home.html')

def about_view(request):
    return render(request, 'shop/about.html')

def contact_view(request):
    return render(request, 'shop/contact.html')
