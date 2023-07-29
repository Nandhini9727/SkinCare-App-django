from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None
    
    if category_slug != None: # to display products by category
        categories = get_object_or_404(Category, slug = category_slug) # returns object that matches slug = category_slug if found otherwise 404 error is shown
        products = Product.objects.filter(category = categories, is_available = True)# The QuerySet returned by all() describes all objects in the database table created by model Prodcut and also it must meet condition is_available=True
    else: # to display all products
        products = Product.objects.all().filter(is_available=True).order_by('id')
    paginator = Paginator(products,3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count() # counts the number of products
    context ={ # defining context dictionary to send it to store.html template
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug,product_slug): # to display product detail
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug = product_slug) # get the object that matches category__slug=category_slug, slug = product_slug
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product= single_product).exists() # cart is the foreign key in CartItem where we need to access cart id from cart. Filter the cart item for that particular product and session
    except Exception as e:
        raise e # if not found it excetion is raised
    context = { # defining context dictionary to send it to product_detail.html template
        'single_product': single_product,
        'in_cart' : in_cart
    }
    return render(request,'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains =keyword))
            product_count = products.count()
        context = {
            'products' : products,
            'product_count' : product_count,
        }
    return render(request,'store/store.html',context)