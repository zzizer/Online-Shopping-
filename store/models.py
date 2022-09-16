from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150, null=True)
    email = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=150, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default = False, blank=False, null=True)
    image = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return self.name
        
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer =models.ForeignKey(Customer,blank=True, null=True,on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete  = models.BooleanField(default = False)
    transaction_id = models.CharField(null=True, max_length=100)
    
    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    
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
        
class OrderItem(models.Model):
    product =models.ForeignKey(Product,blank=True, null=True,on_delete=models.SET_NULL)
    order = models.ForeignKey(Order,blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default = 0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True,on_delete=models.SET_NULL)
    address = models.CharField(null=False, max_length=50)
    city = models.CharField(null=False, max_length=50)
    state = models.CharField(null=False, max_length=50)
    zip_code = models.CharField(null=False, max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
    