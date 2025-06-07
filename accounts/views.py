from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


#VERIFICATION CONFIG

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import EmailMessage
from carts.views import _cart_id
from carts.models import Cart, CartItem


# Create your views here.
def register(request):
    if request.method == 'POST':
        form =RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username =email.split('@')[0]
            user =Account.objects.create_user(first_name=first_name, last_name=last_name,email=email, username=username, password=password) # model = cleaned data
            user.phone_number = phone_number # beacuse we arent using phone number in the model that is why it is added like this here and not in the create_user         
            user.save()

            #USER ACTIVATION  # email isnt sending verfication messages so im going to skip 


            current_site= get_current_site(request)
            email_subject ="please activate your account"
            message =render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),#encoding the primary key so that someone else wont see it
                'token': default_token_generator.make_token(user),
                
            })
            to_email = email
            send_email =EmailMessage(email_subject, message,to=[to_email])
            send_email.send()

        
            messages.success(request, "Registration successful")
            return redirect ('register')

    else:
        form = RegistrationForm()

    context ={
        'form': form,
    }
    return render(request, 'accounts/register.html', context) 


def login(request):
    if request.method == 'POST':
        email = request.POST["email"]# the email in the request.Post["email"] is gotten from the name = email in the forms 
        password = request.POST["password"] # the password in the request.Post["password"] is gotten from the name =" passwords" in the forms
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id =_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # getting product variation by cart id
                    product_variation =[]
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # get the cart items from the user to access his product variation 
                    cart_item = CartItem.objects.filter( user = user)
          
                    ex_var_list =[]
                    id =[]
                    for item in cart_item:
                        existing_variation =item.variations.all()
                        ex_var_list.append(list(existing_variation)) 
                        id.append(item.id)

                    # product_variation =[1, 2, 3, 4, 6]
                    # existing_variation ={4, 6, 3, 5}
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item =CartItem.objects.get(id = item_id)
                            item.quantity +=1
                            item.user = user
                            item.save()

                        else :
                            cart_item = CartItem.objects.filter(cart=cart)
                        
                            for item in cart_item:
                                item.user =user
                                item.save()


            except:
                pass

            auth.login(request,user)
            messages.success(request,'you are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request,'invalid login credentials')
            return redirect('login')

        
    
    return render(request, 'accounts/login.html') 

@login_required(login_url ='login')

def logout(request):
    auth.logout(request)
    messages.success(request,'you have logged out')

    return redirect('login')
    


def activate(request, uidb64, token): # email isnt sending verfication messages so im going to skip 

    try:
        uid =urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None 
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active =True
        user.save()
        messages.success(request,'congratulation your sccount s acctivated ')
        return redirect('login')
    else:
        messages.error('invalid actiavteion link')
        return redirect('register')
   

@login_required(login_url ="login")
def dashboard (request):
    return render (request,"accounts/dashboard.html")