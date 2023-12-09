from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

#registration of models should be done individually
admin.site.register(Cart)
admin.site.register(CartItem)