from django.db import models
from django.utils import timezone
from files.models import Image


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(default = 0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name + " #" + str(self.id)
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    main = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)