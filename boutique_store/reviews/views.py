from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import Review
from products.models import Product
from .forms import ReviewForm

User = get_user_model()

class ReviewListView(View):
    def get(self, request):
        reviews = Review.objects.all()
        return render(request, 'reviews/review_list.html', {'reviews': reviews})

class AddReviewView(View):
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product_id)
        return render(request, 'reviews/add_review.html', {'form': form, 'product': product})
