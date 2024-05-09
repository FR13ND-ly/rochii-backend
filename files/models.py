from django.db import models
from django.utils import timezone

    
class Image(models.Model):
    name = models.CharField(max_length=255)
    contentType = models.CharField(max_length=100)
    data = models.BinaryField()
    date = models.DateTimeField(default=timezone.now)