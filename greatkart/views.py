from django.shortcuts import render
from store.models import Product, ReviewRating,Banner_images

def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    banner = Banner_images.objects.get()

    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
        'banner': banner,
    }
    return render(request, 'home.html', context)