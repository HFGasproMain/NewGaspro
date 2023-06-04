from rest_framework import serializers
from .models import OnboardingOrder, RefillOrder
from billing.models import OrderOnboardBilling
from billing.serializers import OnboardOrderSerializer
from accounts.models import User

class OnboardingOrderSerializer(serializers.ModelSerializer):
	cy_type = (
		('new_cylinder','new_cylinder'),
		('existing_cylinder', 'existing_cylinder')) 
	customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=5))
	cylinder_type = serializers.ChoiceField(choices=cy_type)
	#billing_details = OnboardOrderSerializer()

	class Meta:
		model = OnboardingOrder
		#fields = '__all__'
		fields = ['id', 'cylinder_type', 'state', 'lga', 'home_address', 'customer']
	
	def create(self, validated_data):
		cy_type = validated_data.get('cylinder_type')
		customer = validated_data.get('customer')

		# for new cylinders
		if cy_type == 'new_cylinder':
			#billing_details = validated_data.pop('billing_details')
			order = OnboardingOrder.objects.create(**validated_data)
			OrderOnboardBilling.objects.create(customer=customer, order=order)
			return order
		elif cy_type == 'existing_cylinder':
			#billing_details = validated_data.pop('billing_details')
			order = OnboardingOrder.objects.create(**validated_data)
			gas_cost = 0.0
			cylinder_cost = 0.0
			OrderOnboardBilling.objects.create(customer=customer, order=order, cylinder_cost=cylinder_cost, gas_cost=gas_cost)
			return order


class OnboardedOrderListSerializer(serializers.ModelSerializer):
	# customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=5))
	# cylinder_type = serializers.CharField(max_length=50)
	# billing_details = OnboardOrderSerializer()

	class Meta:
		model = OnboardingOrder
		fields = '__all__'
		


class RefillOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefillOrder
        fields = '__all__'
