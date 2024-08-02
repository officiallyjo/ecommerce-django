from django.shortcuts import render,redirect
from store.models import Product
from .models import Cart,CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

# Helper function to get or create a session ID for the cart
def _cart_id(request):
    # Get the session ID if it exists
    cart = request.session.session_key
    # If the session ID doesn't exist, create a new session
    if not cart:
        cart = request.session.create()
    # Return the session ID
    return cart

# View to add a product to the cart
def add_cart(request, product_id):
    # Get the product by its ID
    product = Product.objects.get(id=product_id)
    
    # Try to get the cart associated with the session ID
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    # If the cart does not exist, create a new cart
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    # Save the cart
    cart.save()
    
    # Try to get the cart item for the given product and cart
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        # If the cart item exists, increment the quantity
        cart_item.quantity += 1
        cart_item.save()
    # If the cart item does not exist, create a new cart item
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
   
    # Redirect to the cart view after adding the item
    return redirect('cart')

# View to display the cart

def cart(request, total=0, quantity=0, cart_items=None): 
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    # Render the cart template
    return render(request, 'store/cart.html', context)