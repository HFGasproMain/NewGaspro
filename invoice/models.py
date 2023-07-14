from django.db import models
from accounts.models import User
from orders.models import RefillOrder
# Create your models here.

class Invoice(models.Model):
    invoice_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refill_order = models.OneToOneField(RefillOrder, on_delete=models.CASCADE)
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2)
    billable_assets_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_id

    class Meta:
    	ordering = ['-date_created']
