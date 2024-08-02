# Importing the necessary models and functions from the current package
from .models import Cart, CartItem
from .views import _cart_id

# Define the counter function, which takes a request as an argument
def counter(request):
    cart_count = 0  # Initialize the cart count to zero
    
    # Check if the request path contains 'admin'
    if 'admin' in request.path:
        return {}  # If the path is for the admin, return an empty dictionary
    
    # If the request path does not contain 'admin'
    else:
        try:
            # Get the cart for the current session using the cart_id
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            
            # Get all cart items associated with the retrieved cart(s)
            # cart[:1] ensures only one cart is passed to the filter
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            
            # Iterate through the cart items and sum up their quantities
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0  # If the Cart does not exist, set cart_count to 0
    
    # Return a dictionary with the cart_count value
    return dict(cart_count=cart_count)
