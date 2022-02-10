
from django.db import models

# Create your models here.


class Account(models.Model):
    cardholder_name = models.CharField(max_length=50, default="", null=True)
    card_number = models.IntegerField()
    expiration_date = models.DateField()
    cvc_number = models.IntegerField()

    def __str__(self):
        return self.cardholder_name
