from django.shortcuts import render, get_object_or_404, redirect
from .models import Product , ReviewRating
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct

# Create your views here.

def store(request, category_slug=None):
    # Initialize variables for categories and products
    categories = None
    products = None 
    
    # Check if a category slug is provided in the URL
    if category_slug is not None:
        # If a category slug is provided, get the category object
        # If the category does not exist, return a 404 error
        categories = get_object_or_404(Category, slug=category_slug)
        
        # Filter the products that belong to the retrieved category and are available
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products,1)
        page = request.GET.get('page')
        paged_products =paginator.get_page(page)
        
        # Count the number of products in the filtered queryset
        product_count = products.count()
    else:
        # If no category slug is provided, get all available products
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,4)
        page = request.GET.get('page')
        paged_products =paginator.get_page(page)
        # Count the total number of available products
        product_count = products.count()
    
    # Prepare the context dictionary to pass data to the template
    context = {
        'products':  paged_products,           # List of products to be displayed
        'product_count': product_count  # Number of products to be displayed
    }
    
    # Render the 'store/store.html' template with the context data
    return render(request, 'store/store.html', context)
  

def product_detail(request,category_slug,product_slug):
    try:
        single_product= Product.objects.get(category__slug= category_slug ,slug =product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product = single_product).exists()
        
    except Exception as e:
        raise  e
        

    try :
        orderproduct = OrderProduct.objects.filter(user=request.user, product_id = single_product.id).exists()
    except OrderProduct.DoesNotExist   :
        orderproduct = None


    #get the reviews 
    reviews = ReviewRating.objects.filter(product_id = single_product.id ,status =True)
        
    context ={
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews' : reviews,
    }

    return render(request,'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context ={
        "products": products,
        "product_count": product_count
        }
    return render(request, 'store/store.html', context)



# def submit_review(request, product_id):
#     url = request.META.get('HTTP_REFERER')
#     if request.method == 'POST':
#         try:
#             reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
#             form = ReviewForm(request.POST, instance=reviews)
#             form.save()
#             messages.success(request, "Thank you! Your review has been updated.")
#             return redirect(url)
#         except ReviewRating.DoesNotExist:
#             form = ReviewForm(request.POST)
#             if form.is_valid():
#                 data = ReviewRating()
#                 data.subject = form.cleaned_data['subject']
#                 data.rating = form.cleaned_data['rating']
#                 data.reviews = form.cleaned_data['reviews']
#                 data.ip = request.META.get('REMOTE_ADDR')
#                 data.product_id = product_id
#                 data.user_id = request.user.id
#                 data.save()
#                 messages.success(request, "Thank you! Your review has been submitted.")
#                 return redirect(url)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            if form.is_valid():
                form.save()
                messages.success(request, "Thank you! Your review has been updated.")
            else:
                print("Update form errors:", form.errors)
                messages.error(request, "Could not update review. Please correct the errors.")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.reviews = form.cleaned_data['reviews']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted.")
            else:
                print("New form errors:", form.errors)
                messages.error(request, "Could not submit review. Please correct the errors.")
            return redirect(url)
