from django.urls import path
from . import views

urlpatterns = [
    # '' is the URL pattern of store page
    # store is the function inside views module that gets called
    # name="store" is the URL pattern name
    path('',views.store,name='store'),
    # to display products by category
    # when parameter is defined inside <>, it is sent to store function inside views Module
    # name="products_by_category" is the URL pattern name
    path('category/<slug:category_slug>/',views.store,name='products_by_category'),
    # to display product detail page
    # when parameter is defined inside <>, it is sent to product_detail function inside views Module
    # name="product_detail" is the URL pattern name
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name = 'product_detail'),
    path('search/',views.search, name= 'search'),
]