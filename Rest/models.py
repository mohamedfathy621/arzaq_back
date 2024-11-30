from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    titles = models.CharField(max_length=255)
    description = models.CharField()
    email = models.CharField(max_length=100)
    image_url = models.CharField(max_length=255)
    def __str__(self):
        return self.username
