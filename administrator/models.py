from django.db import models
from django.utils import timezone
import uuid


class User(models.Model):
    username = models.CharField(max_length=150, unique=True, db_index=True)
    password = models.TextField() 
    date = models.DateTimeField(default=timezone.now)


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date = models.DateTimeField(default=timezone.now)
