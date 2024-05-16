from django.db import models

# Create your models here.
# models.py

from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField( null=True, blank= True)
    mobile = models.BigIntegerField(null=True, blank= True)
