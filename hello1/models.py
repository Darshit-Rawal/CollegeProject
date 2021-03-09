from django.db import models
from django.db import connections

# Create your models here.

class User(models.Model):   
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    userType = models.CharField(max_length=100)
    organizationName = models.CharField(max_length=100)
 
    class Meta:
        db_table = "logintable"
