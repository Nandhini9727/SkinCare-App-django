from django.urls import path
from . import views

urlpatterns =[
    # '' is the URL pattern of cart page
    # cart is the function inside views module that gets called
    # name="cart" is the URL pattern name
    path('',views.cart, name='cart'),
    # to display products added to cart
    # when parameter is defined inside <>, it is sent to add_cart function inside views Module
    # name="add_cart" is the URL pattern name
    path('add_cart/<int:product_id>/',views.add_cart, name = 'add_cart'),
    # to decrement or remove a product from cart
    # when parameter is defined inside <>, it is sent to remove_cart function inside views Module
    # name="remove_cart" is the URL pattern name
    path('remove_cart/<int:product_id>/',views.remove_cart, name = 'remove_cart'),
    # to remove a product from cart
    # when parameter is defined inside <>, it is sent to remove_cart_item function inside views Module
    # name="remove_cart_item" is the URL pattern name
    path('remove_cart_item/<int:product_id>/',views.remove_cart_item, name = 'remove_cart_item'),
    path('checkout/', views.checkout, name = 'checkout'),
]