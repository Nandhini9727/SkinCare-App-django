import os
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail  import EmailMessage
from django.contrib.auth.decorators import login_required
from carts.models import Cart, CartItem
from carts.views import _cart_id

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)#request.POST will contain all the post values
        if form.is_valid(): #checks if form as all the required fields
            first_name = form.cleaned_data['first_name'] # In django to fetch values from request we used cleaned_data
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0] #creating username from email 
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username) # creating Account objects once we fetch all the values from POST request
            user.phone_number = phone_number # since phone number is not used in create_user method. we need to give it this way
            user.save()
            #user activation
            current_site = get_current_site(request) # to get the domain
            mail_subject = 'Please Activate Your Account'
            #sending mail using html and also sending context we need
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),#encoding the user id so that no body sees it
                'token': default_token_generator.make_token(user), # create token for user
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm() #form object is created by using RegistrationForm class
    context ={
        'form': form,
        }
    return render(request, 'accounts/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email'] # getting the email from request
        password = request.POST['password']
        user = auth.authenticate(email= email, password=password) # checks if we have the user registered
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id= _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart = cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart = cart)
                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request,user)
            #messages.success(request,'Your logged in')
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('home')
        else:
           messages.error(request,'Invalid login credential') 
           return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url='login') #only if logged in we can use logout
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() #decode the user id 
        user = Account._default_manager.get(pk=uid) # getting the account of user using user id
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):#checking if user is true and also token exist
        user.is_active = True # setting the status to true will register the user and also allows login
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request,'Password reset email has been set to your email address')
            return redirect('login')
        else:
            messages.error(request, 'Account Does Not Exists')
            return redirect('forgotPassword')

    return render(request,'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']= uid
        messages.success(request, 'Please Reset Your Password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Link is expired')
        return redirect('login')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Reset successful ')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('resetPassword')
    else:
        return render(request,'accounts/resetPassword.html')
