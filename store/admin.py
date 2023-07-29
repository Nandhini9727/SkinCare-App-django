from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    # to display model object with multiple field instead of a single field
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    # to prepopulate the slug field by product_name field
    prepopulated_fields = {'slug': ('product_name',)}
# Register the Product and ProductAdmin Model in admin.py to be able to see it in admin panel
admin.site.register(Product,ProductAdmin )