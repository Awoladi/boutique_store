from django.shortcuts import render, redirect
from django.http import HttpResponse

def checkout_page(request):
    # Render the checkout page
    return render(request, 'checkout/checkout.html')

def process_checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # Process the checkout (e.g., save order details, validation, etc.)

        # After processing, redirect back to the checkout page
        return redirect('checkout:checkout_page')  # Redirects to the checkout page

    return HttpResponse("Invalid Request", status=400)

def success_page(request):
    # Render the success page
    return render(request, 'checkout/checkout_success.html')
