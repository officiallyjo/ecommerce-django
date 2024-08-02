from django.shortcuts import render, get_object_or_404
from .models import Product 
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

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
        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products,3)
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
    context ={
        'single_product': single_product,
        'in_cart': in_cart,
    }

    return render(request,'store/product_detail.html',context)