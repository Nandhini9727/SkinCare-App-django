from django.contrib import admin
from .models import Category

# to create perpopulated fields
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug':('category_name',)}
    # to display fields in model objects in front pge of table
    list_display = ('category_name','slug')

# Register your models here.
# Register the Category Model in admin.py to be able to see it in admin panel
admin.site.register(Category, CategoryAdmin)