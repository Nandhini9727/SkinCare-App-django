from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.

class Product(models.Model):
    # list of all the fields that we neeed for Product model
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(max_length=500,blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    # to make Category model a foreign key
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # models.CASCADE is used for deleting all product related to particular category that is deleted
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now = True)

    def get_url(self): 
        return reverse('product_detail',args=[self.category.slug,self.slug]) # return URL path of particular product

    def __str__(self): # The __str__ method just tells Django what to print when it needs to print out an instance of the any model.
        return self.product_name
