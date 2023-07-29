# view is created by developer and is not included when project is created
from django.shortcuts import render
from store.models import Product

def home(request): # functions inside view always take request as parameter
    products = Product.objects.all().filter(is_available=True) # The QuerySet returned by all() describes all objects in the database table created by model Prodcut and also it must meet condition is_available=True
    # defining the context dictionary
    context = {
        'products': products,
    }
    # render is used to combine the template 'home.html' with the context dictionary and return HTTP Response oject
    # request is the request object which is used to generate this response
    # 'home.html' is the template name
    # context is the context dictionary that is sent to the template to add to template context
    return render(request, 'home.html',context)