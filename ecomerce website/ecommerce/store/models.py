from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# build Customer model
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    # will show user name when open admin page to edit
    def __str__(self) -> str:
        return self.name
# build Product model
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True) #need download Pillow library so we can add ImageField to our models

    # will show user name when open admin page to edit
    def __str__(self) -> str:
        return self.name
    # ADD THIS PROPERTY TO MAKE SURE IF IMAGE IS NOT UPLOADED, THE WHOLE PAGE STILL LOAD
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

# build Order model
class Order(models.Model):
    # SET_NULL: when delete the order, customer wont be deleted, instead show as null
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    # if order not complete, we can still add product to it => control if any more product can be added to the cart
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital ==False:
                shipping = True
        return shipping


    # when edit in admin page, show order id
    def __str__(self) -> str:
        # watchout the return data type, this is __str__, return need to be string
        return str(self.id)

# OrderItem model to track products in the order
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self) -> str:
        return self.product.name
    
# create ShippingAddress model for orders needed shipped
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.address