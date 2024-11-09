from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Medications(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    dosage_form = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100)
    concentration = models.CharField(max_length=100)
    price =  models.DecimalField(max_digits=5, decimal_places=2)
    refill_requests = models.IntegerField()
    refills_issued = models.IntegerField()
    image_url = models.CharField(max_length=255)
    def __str__(self):
        return self.username

class Refill_orders(models.Model):
    user_id= models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField(auto_now=True)
    orderlist = models.JSONField()
    TotalPrice= models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.username
class Admins(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)