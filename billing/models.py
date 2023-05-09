from django.db import models
from orders.models import OnboardingOrder
from accounts.models import User

# Create your models here.
class OrderOnboardBilling(models.Model):
	customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_onboard_order')
	order = models.OneToOneField(OnboardingOrder, on_delete=models.CASCADE, related_name='onboarded_order')
	annual_sub = models.DecimalField(max_digits=8, decimal_places=2, default=10000.00)
	cylinder_fee = models.DecimalField(max_digits=8, decimal_places=2, default=18000.00, blank=True, null=True)
	gas_fee = models.DecimalField(max_digits=8, decimal_places=2, default=9600.00, blank=True, null=True)
	biller = models.CharField(max_length=50, null=True, blank=True, default='Homefort Delivery Staff')
	total_cost = models.CharField(max_length=20, blank=True, null=True, default='00.00', editable=False)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.id

	def save(self, *args, **kwargs):
		self.total_cost = self.annual_sub + self.cylinder_cost + self.gas_cost
		super(OrderOnboardBilling, self).save(*args, **kwargs)

	def get_cost(self):
		return Decimal(self.annual_sub) + Decimal(self.cylinder_cost) + Decimal(self.gas_cost)

	class Meta:
		ordering = ['-date_created']



	'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_transaction")
    gas_order = models.ForeignKey(GasOrder, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS, default="Pending")
    delivery_guy = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name="delivery_transaction")
    transaction_date = models.DateField(auto_now_add=True)
    access_code = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return str(self.id)
    '''