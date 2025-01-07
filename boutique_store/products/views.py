from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Category, Review
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from products.forms import ReviewForm

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Product, Category

class CategoryProductListView(ListView):
    model = Product
    template_name = 'products/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=category_slug)
        return Product.objects.filter(category=category)

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
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
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