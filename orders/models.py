from django.db import models
from products.models import Product
from django.utils import timezone


class Order(models.Model):
    username = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    details = models.TextField(blank=True)
    completed = models.BooleanField(default = False)
    date = models.DateField(default=timezone.now)
    hour = models.PositiveIntegerField()
    createdDate = models.DateTimeField(default=timezone.now)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    
