
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from products.models import Product, Category
from .forms import ProductForm


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


def shop_view(request):
    category_slug = request.GET.get('category')  # Capture category from URL
    categories = Category.objects.all()  # Fetch all categories
    products = Product.objects.all()  # Fetch all products initially

    if category_slug:  # Apply filter if a category is selected
        products = products.filter(category__slug=category_slug)

    return render(request, 'shop/index.html', {
        'products': products,
        'categories': categories
    })

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop:shop_index')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/edit_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect('shop:shop_index')
    return render(request, 'shop/delete_product.html', {'product': product})