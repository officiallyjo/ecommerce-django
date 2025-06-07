from django.shortcuts import render,redirect, get_object_or_404

from store.models import Product,Variation
from .models import Cart,CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

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
    current_user = request.user
    # Get the product by its ID
    product = Product.objects.get(id=product_id)

    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation =[]

    

        if request.method == 'POST':
            for item in request.POST:
                key =item
                value = request.POST[key]
                

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        
        
        is_cart_item_exists = CartItem.objects.filter(product=product, user = current_user).exists()
        # Try to get the cart item for the given product and cart
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user = current_user)
          
            ex_var_list =[]
            id =[]
            for item in cart_item:
                existing_variation =item.variations.all()
                ex_var_list.append(list(existing_variation)) 
                id.append(item.id)

            if product_variation in ex_var_list:
                # add cart item quantity
                index =ex_var_list.index(product_variation)
                item_id =id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

                # create new cart item
            else:
                item = CartItem.objects.create(product=product,quantity=1,user = current_user)
                if len(product_variation) > 0:
                    item.variations.clear()  # Remove any existing variations before adding new ones
                    item.variations.add(*product_variation)
                item.save()
        # If the cart item does not exist, create a new cart item
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user = current_user ,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()  # Remove any existing variations before adding new ones
                cart_item.variations.add(*product_variation)
            cart_item.save()
        
        # Redirect to the cart view after adding the item
        return redirect('cart')
    
    #if user is not authenticated

    else :
        product_variation =[]

    

        if request.method == 'POST':
            for item in request.POST:
                key =item
                value = request.POST[key]
                

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        
        # Try to get the cart associated with the session ID
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        # If the cart does not exist, create a new cart
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        # Save the cart
        cart.save()
        
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        # Try to get the cart item for the given product and cart
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing variations -> from data base
            # current variation -> product variation
            # item id -> from datatbase

            # If the current variation is in the existing variations, add it to the cart item then increase the quamtity of the cart item
            ex_var_list =[]
            id =[]
            for item in cart_item:
                existing_variation =item.variations.all()
                ex_var_list.append(list(existing_variation)) 
                id.append(item.id)

            if product_variation in ex_var_list:
                # add cart item quantity
                index =ex_var_list.index(product_variation)
                item_id =id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

                # create new cart item
            else:
                item = CartItem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()  # Remove any existing variations before adding new ones
                    item.variations.add(*product_variation)
                item.save()
        # If the cart item does not exist, create a new cart item
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()  # Remove any existing variations before adding new ones
                cart_item.variations.add(*product_variation)
            cart_item.save()
        
        # Redirect to the cart view after adding the item
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    # the original code wasnt working so chat gpt modified it to the one that conatins filter instead and it worked
    #  cart = Cart.objects.get(cart_id =_cart_id(request))  - original code 

    cart = Cart.objects.filter(cart_id =_cart_id(request)).first()  #chatgpt version
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        
        else :
            cart = Cart.objects.get(cart_id =_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete() 
    except:
         pass
            
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):

    # the original code wasnt working so chat gpt modified it to the one that conatins filter instead and it worked
    # cart = Cart.objects.get(cart_id =_cart_id(request))  - original code

    cart = Cart.objects.filter(cart_id =_cart_id(request)).first()  #chatgpt version
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user ,id=cart_item_id)

    else:
        cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
    cart_item.delete()
    
    return redirect('cart')
# View to display the cart

# d ef cart(request, total=0, quantity=0, cart_items=None): 
    # tax = 0
    # grand_total = 0

    # if request.user.is_authenticated:
    #     cart_items = CartItem.objects.filter(user=request.user, is_active=True)

    # else:
    #     try:
    #         cart = Cart.objects.get(cart_id=_cart_id(request))
    #         cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    #         for cart_item in cart_items:
    #             total += (cart_item.product.price * cart_item.quantity)
    #             quantity += cart_item.quantity
    #         tax = (2 * total) / 100
    #         grand_total = total + tax
    #     except ObjectDoesNotExist:
    #         pass

    # context = {
    #     'total': total,
    #     'quantity': quantity,
    #     'cart_items': cart_items,
    #     'tax': tax,
    #     'grand_total': grand_total
    # }
    # # Render the cart template
    # return render(request, 'store/cart.html', context)



def cart(request, total=0, quantity=0, cart_items=None): 
    tax = 0
    grand_total = 0

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        except ObjectDoesNotExist:
            cart_items = []

    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    tax = (2 * total) / 100
    grand_total = total + tax

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    
    return render(request, 'store/cart.html', context)



@login_required(login_url="login")
def checkout(request, total=0, quantity=0, cart_items=None):
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
    return render(request,'store/checkout.html', context)