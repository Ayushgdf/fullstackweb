from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.
class about(models.Model):
    name=models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    number=models.CharField(max_length=122)
    feedback=models.TextField()
    date=models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    def __str__(self):
        return self.username