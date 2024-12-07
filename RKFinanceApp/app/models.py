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


class Cement(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    mobile = models.BigIntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class Oil(models.Model):
    name = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=100,choices=(("PETROL","petrol"),("DIESEL","diesel"),("GAS","gas"),("FORTUNE SUNLITE REFINED SUNFLOWER OIL","fortune sunlite refined sunflower oil")))
    email = models.EmailField(null=True, blank=True)
    mobile = models.BigIntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class Withdraw(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    amount = models.FloatField()



class Client(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="transactions")
    date = models.DateTimeField(auto_now=True)
    remarks = models.CharField(max_length=255)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True)

    def __str__(self):
        return f"{self.client.name} on {self.date}"

