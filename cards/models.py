from django.db import models
from accounts.models import User
# Create your models here.

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)
    pin = models.IntegerField(null=True)

    def __str__(self):
        return self.card_number
