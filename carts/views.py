from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.



def _cart_id(request): # to get the session key and _ before function name makes it private function
    cart = request.session.session_key
    if not cart:
        cart = request.session.create() # to create new session key
    return cart

def add_cart(request, product_id):
    current_user = request.user
    if(current_user.is_authenticated):
        product = Product.objects.get(id = product_id) # get product object by product id
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if(is_cart_item_exists):
            cart_item = CartItem.objects.get(product=product, user=current_user) # get the cart item that is already in cart
            cart_item.quantity += 1 # Need to increment quantity as we are adding a product to cart
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user) # create a cart item if the cart does not have that particular product in cart
        cart_item.save()
        return redirect('cart')
    else:
        product = Product.objects.get(id = product_id) # get product object by product id
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request)) # getting the cart id or session key by _cart_id function
        except Cart.DoesNotExist :
            cart = Cart.objects.create(cart_id = _cart_id(request)) # if the object does not exist create new project
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart) # get the cart item that is already in cart
            cart_item.quantity += 1 # Need to increment quantity as we are adding a product to cart
        except CartItem.DoesNotExist :
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart) # create a cart item if the cart does not have that particular product in cart
        cart_item.save()
        return redirect('cart')

def remove_cart(request, product_id):#this is to remove a cart item by quantity using decrement button
    current_user = request.user
    if(current_user.is_authenticated):
        product = get_object_or_404(Product, id=product_id) # get the product of object that we need to remove
        cart_item = CartItem.objects.get(product=product, user = current_user) # get the cart item of object that we need to remove
        if cart_item.quantity > 1: # if there are more than one product just decrease the quantity
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete() # if there is only one product delete the cart item
        return redirect('cart')
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        product = get_object_or_404(Product, id=product_id) # get the product of object that we need to remove
        cart_item = CartItem.objects.get(product=product, cart= cart) # get the cart item of object that we need to remove
        if cart_item.quantity > 1: # if there are more than one product just decrease the quantity
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete() # if there is only one product delete the cart item
        return redirect('cart')

def remove_cart_item(request, product_id):#this is to remove a cart item by using remove button
    current_user = request.user
    if(current_user.is_authenticated):
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, user= current_user)
        cart_item.delete()
        return redirect('cart')
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart= cart)
        cart_item.delete()
        return redirect('cart')

def cart(request, total =0, quantity=0, cart_items= None): # to get all item in cart page
    try:
        tax = 0
        grand_total = 0
        if(request.user.is_authenticated):
            cart_items = CartItem.objects.filter(user=request.user,is_active=True) # get all items in car
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request)) # get the session key
            cart_items = CartItem.objects.filter(cart=cart, is_active=True) # get all items in cart
        for cart_item in cart_items:
            total += (cart_item.product.price * (cart_item.quantity)) # calculate the total price
            quantity += cart_item.quantity
        tax = (2 * total)/100 # calculate tax
        grand_total = total + tax # tax + total
    except ObjectDoesNotExist:
        pass 

    context ={ # defining context dictionary to send it to cart.html template
        'total' : total, 
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request,'store/cart.html',context)
@login_required(login_url='login') #force you to login before you can checkout
def checkout(request, total =0, quantity=0, cart_items= None):
    try:
        tax = 0
        grand_total = 0
        current_user = request.user
        if(current_user.is_authenticated):
            cart_items = CartItem.objects.filter(user=current_user, is_active=True) # get all items in cart
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request)) # get the session key
            cart_items = CartItem.objects.filter(cart=cart, is_active=True) # get all items in cart
        for cart_item in cart_items:
            total += (cart_item.product.price * (cart_item.quantity)) # calculate the total price
            quantity += cart_item.quantity
        tax = (2 * total)/100 # calculate tax
        grand_total = total + tax # tax + total
    except ObjectDoesNotExist:
        pass 

    context ={ # defining context dictionary to send it to cart.html template
        'total' : total, 
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/checkout.html',context)