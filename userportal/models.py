from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length = 250)
    price = models.IntegerField()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    buy =  models.BooleanField()

    @property
    def get_cart_total(self):
        orderdish = self.orderproduct_set.all()
        sum=0
        for item in orderdish:
            sum = sum + item.get_total
        return sum

    @property
    def get_cart_items(self):
        orderdish = self.orderproduct_set.all()
        sum=0
        for item in orderdish:
            sum = sum + item.quantity
        return sum


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)


    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total