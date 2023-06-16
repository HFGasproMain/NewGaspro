from rest_framework import serializers
from .models import OnboardingOrder, RefillOrder
from billing.models import OrderOnboardBilling
from billing.serializers import OnboardOrderSerializer
from accounts.models import User
from auxilliary.models import Auxiliary

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
	user_full_name = serializers.SerializerMethodField()
	user_address = serializers.SerializerMethodField()
	user_phone_number = serializers.SerializerMethodField()

	def get_user_full_name(self, obj):
		return obj.user.get_full_name()

	def get_user_address(self, obj):
		return obj.user.address  

	def get_user_phone_number(self, obj):
		return obj.user.phone_number  

	class Meta:
		model = RefillOrder
		fields = ['id', 'user_full_name', 'user_address', 'user_phone_number', 'smart_box', 'date_created','status']
		#fields = '__all__'



class RefillOrderDetailSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()
    user_address = serializers.SerializerMethodField()
    user_phone_number = serializers.SerializerMethodField()
    user_class = serializers.SerializerMethodField()
    auxiliary_full_name = serializers.SerializerMethodField()
    auxiliary_phone_number = serializers.SerializerMethodField()
    cylinder_type = serializers.SerializerMethodField()

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()

    def get_user_address(self, obj):
        return obj.user.address  # Replace 'address' with the actual field name

    def get_user_phone_number(self, obj):
        return obj.user.phone_number  # Replace 'phone_number' with the actual field name

    def get_user_class(self, obj):
        return obj.user.user_class  # Replace 'user_class' with the actual field name

    def get_auxiliary_full_name(self, obj):
        auxiliary = obj.user.user_auxiliary
        return auxiliary.get_full_name() if auxiliary else None

    def get_auxiliary_phone_number(self, obj):
        auxiliary = obj.user.user_auxiliary
        return auxiliary.get_phone_number() if auxiliary else None

    def get_cylinder_type(self, obj):
    	return obj.cylinder.cylinder_capacity 

 

    class Meta:
        model = RefillOrder
        fields = ['id', 'user_full_name', 'user_address', 'user_phone_number', 'user_class', 'smart_box', 'cylinder', 'cylinder_type', 
        	'order_id', 'status', 'access_code', 'transaction_id', 'date_created', 'auxiliary_full_name', 'auxiliary_phone_number']

