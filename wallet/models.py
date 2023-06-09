from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model() 


# Create your models here.
class Wallet(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_wallet')
	balance = models.DecimalField(decimal_places=2, max_digits=8, default=0.0)
	debt = models.DecimalField(decimal_places=2, max_digits=8, default=0.0)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.balance)
