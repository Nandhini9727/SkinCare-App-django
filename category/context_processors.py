from .models import Category

# to make use of category fields in any templates we want
def menu_links(request):
    links = Category.objects.all()# The QuerySet returned by all() describes all objects in the database table created by model Category
    return dict(links = links) # dictionary object is returned