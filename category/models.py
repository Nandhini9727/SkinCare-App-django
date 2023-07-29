from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model): # creating class Category or model Category. Each model is a Python class that subclasses django.db.models.Model.
    #Each attribute of the model represents a database field.
    category_name = models.CharField(max_length=50, unique=True) #CharField is generally used for storing small strings like first name, last name, etc. 
    slug = models.SlugField(max_length= 100, unique=True) # A "slug" is a way of generating a valid URL, generally using data already obtained. For instance, in our case a slug uses the category name to generate a URL.
    description = models.TextField(max_length=255, blank=True) # TextField is a large text field for large-sized text. TextField is generally used for storing paragraphs and all other text data. 
    cat_image = models.ImageField(upload_to='photos/category',blank=True) # ImageField is a FileField with uploads restricted to image formats only and ImageField requires pillow to be installed to be usable.

    class Meta: # This inner class Meta is used to change to change the behavior of your model fields like changing order options,verbose_name, and a lot of other options.
        verbose_name = 'category' # singular name of model
        verbose_name_plural = 'categories' # Need to explicitly set the attribute verbose_name_plural on a Model,otherwise Django adds 's' to the name of the model when displaying the name in the admin panel.

    def get_url(self): # it returns the URL of particular category
        return reverse('products_by_category', args=[self.slug]) 

    def __str__(self): # The __str__ method just tells Django what to print when it needs to print out an instance of the any model.
        return self.category_name