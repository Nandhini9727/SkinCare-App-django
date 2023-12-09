from django.db import models
from store.models import Product
from accounts.models import Account
# Create your models here.
class Cart(models.Model): # create Cart Model
    # list of all the fields that we neeed for Cart model
    cart_id = models.CharField(max_length=250, blank=True, null = True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self): # The __str__ method just tells Django what to print when it needs to print out an instance of the any model.
        return self.cart_id

class CartItem(models.Model):
     # list of all the fields that we need for CartItem model
    # to make Product model and Cart model foreign keys
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # models.CASCADE is used for deleting all cart item related to that particular product that is deleted
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE ,null=True, blank=True) # models.CASCADE is used for deleting all cart item if cart that is deleted
    quantity = models.IntegerField()#cart quantity
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        return self.product.price * self.quantity
    def __str__(self): # The __str__ method just tells Django what to print when it needs to print out an instance of the any model.
        return self.product.product_name
