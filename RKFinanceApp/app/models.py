from django.db import models

# Create your models here.
# models.py

from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField( null=True, blank= True)
    mobile = models.BigIntegerField(null=True, blank= True)

class Feedback(models.Model):
    name = models.CharField(max_length=100,null=True, blank= True)
    email =  models.EmailField( null=True, blank= True)
    mobile = models.BigIntegerField(null=True, blank= True)
    is_satisfy = models.BooleanField(default=True)
    feedback = models.TextField(null=True, blank= True,default="No feedback")
    created_at = models.DateTimeField(auto_now_add=True)
