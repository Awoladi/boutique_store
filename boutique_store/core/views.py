from django.shortcuts import render
from .models import SiteSettings
from products.models import Product, Category

def home_page(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'core/home.html', {'products': products, 'categories': categories})
def home(request):
    return render(request, 'core/base.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def site_settings(request):
    settings = SiteSettings.objects.first()
    return render(request, 'core/site_settings.html', {'settings': settings})


def handler404(request, exception):
    """Return custom 404 Not Found page."""
    return render(request, 'core/404.html', {}, status=404)

def handler500(request):
    """Return custom 500 Internal Server Error page."""
    return render(request, 'core/500.html', {}, status=500)
