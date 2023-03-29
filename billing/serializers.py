from rest_framework import serializers
from .models import OrderOnboardBilling


class OnboardOrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderOnboardBilling
		fields = "__all__"
	#fields = ['customer', 'order', 'annual_sub', 'cylinder_cost', 'gas_cost', 'biller', 'total_cost', 'date_created']