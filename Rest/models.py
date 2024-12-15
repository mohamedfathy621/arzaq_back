from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    username=models.CharField(max_length=100,default='')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    titles = models.CharField(max_length=255,default='')
    description = models.TextField(default='')
    email = models.CharField(max_length=100)
    Phone_number = models.CharField(max_length=100,default='###')
    image_url = models.CharField(max_length=255,default='')
    def __str__(self):
        return self.username
