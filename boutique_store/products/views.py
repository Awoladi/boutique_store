from django.views.generic import ListView, DetailView
from .models import Product
from django.shortcuts import render

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'

def product_list(request):
    products = Product.objects.all()
    return render(request, 'list.html', {'products': products})