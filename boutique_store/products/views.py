from django.views.generic import ListView, DetailView, TemplateView
from matplotlib.pyplot import xticks

from .models import Product, Category, Review
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from products.forms import ReviewForm
from pytrends.request import TrendReq
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
import matplotlib.pyplot as plt
import io
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend suitable for servers
from django.http import HttpResponse


def trending_products_chart(request):
    pytrends = TrendReq(hl='en-US', tz=360)

    # Get the number of products to display from the dropdown (default 3)
    num_products = int(request.GET.get('num_products', 3))
    num_products = max(1, min(num_products, 5))  # Limit between 1 and 5 products

    # Fetch all product names from the database
    products = list(Product.objects.values_list('name', flat=True))

    if len(products) < num_products:
        return HttpResponse(f"Not enough products to analyze. ({len(products)} available)", content_type="text/plain")

    # Store data for normalization and trend differences
    trend_differences = {}
    normalized_data = {}
    date_data = None  # To store the date data separately

    try:
        # Fetch data individually for each product and normalize the trends
        for product in products:
            pytrends.build_payload(kw_list=[product], timeframe='today 3-m')
            data = pytrends.interest_over_time().reset_index()

            if date_data is None:
                date_data = data['date']  # Save the date for the x-axis

            if product in data.columns and not data[product].isnull().all():
                # Normalize each product individually
                max_value = data[product].max()
                normalized_data[product] = (data[product] / max_value) * 100
                trend_differences[product] = data[product].iloc[-1] - data[product].iloc[0]

        # Select the top N products with the highest trend increase
        top_products = sorted(trend_differences, key=trend_differences.get, reverse=True)[:num_products]

    except Exception as e:
        return HttpResponse(f"Error fetching Google Trends data: {e}")

    # Plot the normalized data for the selected products with proper date formatting
    plt.figure(figsize=(12, 6))
    for product in top_products:
        plt.plot(date_data, normalized_data[product], label=f'{product} - Normalized Trend Increase')

    # Adjust the x-axis to show dates clearly
    plt.gcf().autofmt_xdate()
    plt.xlabel('Date')
    plt.ylabel('Normalized Trend Score')
    plt.title(f'Top {num_products} Trending Products by Increase in Search Interest')
    xticks(rotation=30)

    # **Legend in Upper Left**
    plt.legend(loc='upper left')

    # Save the plot to a buffer and return the image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return HttpResponse(buffer.getvalue(), content_type='image/png')


# **New View for the Dropdown Menu**
def trending_products_page(request):
    return render(request, 'products/trending_products_dropdown.html')
class CategoryProductListView(ListView):
    model = Product
    template_name = 'products/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        print(f"Category Slug: {category_slug}")  # Debugging slug
        category = get_object_or_404(Category, slug=category_slug)
        print(f"Category: {category}")  # Debugging category object
        products = Product.objects.filter(category=category)
        print(f"Products: {products}")  # Debugging products
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category_name'] = get_object_or_404(Category, slug=self.kwargs.get('slug')).name
        return context

class CategoryListView(TemplateView):
    template_name = 'products/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    paginate_by = 'products'
    paginate_by = 10  # Number of products per page

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        if category_slug:
            return Product.objects.filter(category__slug=category_slug)
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

 # Custom pagination logic
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            products = paginator.page(paginator.num_pages)
        except ValueError:
            # Catch invalid page values
            products = paginator.page(1)

        context['products'] = products
        context['categories'] = categories
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()  # Form added to context correctly
        context['reviews'] = self.object.reviews.all()
        return context


def submit_review(request, pk):
    """Ensure review form works without import errors."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ReviewForm()
    return render(request, 'products/product_detail.html', {'form': form, 'product': product})

def category_products(request, slug):
    print(f"Slug: {slug}")  # Debug slug
    category = get_object_or_404(Category, slug=slug)
    print(f"Category: {category}")  # Debug category
    products = Product.objects.filter(category=category)
    print(f"Products: {products}")  # Debug products
    return render(request, 'products/category_products.html', {
        'category': category,
        'products': products
    })


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # Link the product to the logged-in user
            product.save()
            return redirect('products:product_list')  # Redirect to the product list
    else:
        form = ProductForm()
    return render(request, 'products/product_create.html', {'form': form})

@login_required
def product_edit(request, pk):
    product = Product.objects.get(pk=pk, user=request.user)  # Ensure the product belongs to the user
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_edit.html', {'form': form})

@login_required
def product_delete(request, pk):
    product = Product.objects.get(pk=pk, user=request.user)  # Ensure the product belongs to the user
    if request.method == 'POST':
        product.delete()
        return redirect('products:product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:category_list')
    else:
        form = CategoryForm()
    return render(request, 'products/category_form.html', {'form': form})

@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('products:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'products/category_form.html', {'form': form})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('products:category_list')
    return render(request, 'products/category_confirm_delete.html', {'category': category})