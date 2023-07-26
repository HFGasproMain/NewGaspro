from rest_framework import serializers
from .models import OnboardingOrder, RefillOrder, RefillOrderAssignDeliveryOfficer
from billing.models import OrderOnboardBilling
from billing.serializers import OnboardOrderSerializer
from accounts.models import User
from delivery.models import DeliveryOfficer
from auxilliary.models import Auxiliary
from rest_framework import serializers
from asset.models import Cylinder, OtherBillableAssets, GasPrice


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
	user_lga = serializers.SerializerMethodField()
	user_phone_number = serializers.SerializerMethodField()
	user_cylinder_type = serializers.SerializerMethodField()

	def get_user_full_name(self, obj):
		return obj.user.get_full_name()

	def get_user_address(self, obj):
		return obj.user.address

	def get_user_lga(self, obj):
		return obj.user.lga  

	def get_user_phone_number(self, obj):
		return obj.user.phone_number 

	def get_user_cylinder_type(self, obj):
		return obj.cylinder.cylinder_capacity

	class Meta:
		model = RefillOrder
		fields = ['id', 'user_full_name', 'user_address', 'user_lga', 'user_phone_number', 'smart_box', 'user_cylinder_type',
		 'transaction_id', 'order_id', 'date_created','status', 'action','action_date']
		#fields = '__all__'

	def validate(self, data):
		# Get the refill order and delivery officer data
		refill_order = self.instance
		delivery_officer = data.get('delivery_officer')

		# Check if refill order and delivery officer exist
		if refill_order and delivery_officer:
			# Check if the user LGA matches the delivery officer's retailer business LGA
			if refill_order.user.lga != delivery_officer.retailer.business_lga:
				raise serializers.ValidationError("Refill order user LGA does not match delivery officer's retailer business LGA.")
		return data



class RefillOrderAcceptSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=[('accept', 'Accept'), ('reschedule', 'Reschedule')])
    action_date = serializers.DateField()

    class Meta:
    	model = RefillOrder
    	fields = ['id', 'transaction_id', 'action', 'action_date']


class RefillOrderDeliveryAssignSerializer(serializers.ModelSerializer):
	refill_order = serializers.SerializerMethodField()
	delivery_officer = serializers.PrimaryKeyRelatedField(queryset=DeliveryOfficer.objects.all())

	class Meta:
		model = RefillOrder
		fields = ['refill_order', 'delivery_officer']


# Nested serializer for customer information
class CustomerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    phone_number = serializers.CharField(source='user.phone_number')
    address = serializers.CharField(source='user.address')

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    class Meta:
        model = RefillOrder
        fields = ['full_name', 'phone_number', 'address']

# Main serializer
# class RefillOrderDeliveryAcceptSerializer(serializers.ModelSerializer):
#     action = serializers.ChoiceField(choices=[('accept', 'Accept'), ('reject', 'Reject')])
#     customer_info = CustomerSerializer(source='*')

#     class Meta:
#         model = RefillOrder
#         fields = ['action', 'customer_info']

class RefillOrderDeliveryAcceptSerializer(serializers.ModelSerializer):
	action = serializers.ChoiceField(choices=[('accept', 'Accept'), ('reject', 'Reject')])
	#delivery_officer = serializers.PrimaryKeyRelatedField(queryset=DeliveryOfficer.objects.all())

	class Meta:
		model = RefillOrder
		fields = ['action']


class UserDeliveryHistorySerializer(serializers.ModelSerializer):
    delivery_officer_name = serializers.SerializerMethodField()
    capacity_delivered = serializers.DecimalField(source='new_cylinder.cylinder_capacity', max_digits=5, decimal_places=2, default=None)
    gas_price_per_kg = serializers.DecimalField(source='gas_price.current_price', max_digits=5, decimal_places=2, default=None)
    invoice_amount = serializers.DecimalField(source='invoice.invoice_amount', max_digits=10, decimal_places=2, default=None)

    def get_delivery_officer_name(self, obj):
        return obj.delivery_officer.get_full_name() if obj.delivery_officer else None

    class Meta:
        model = RefillOrder
        fields = ['capacity_delivered', 'gas_price_per_kg', 'delivery_officer_name', 'invoice_amount']


class User1DeliveryHistorySerializer(serializers.ModelSerializer):
    delivery_officer_name = serializers.SerializerMethodField()
    cylinder_type = serializers.SerializerMethodField()

    def get_delivery_officer_name(self, obj):
        return obj.delivery_officer.get_full_name()

    def get_cylinder_type(self, obj):
    	return obj.cylinder.cylinder_capacity

    def get_cylinder_type(self, obj):
    	return obj.cylinder.cylinder_capacity

    class Meta:
        model = RefillOrder
        fields = ['cylinder_type', 'cost_of_gas', 'delivery_officer_name', 'date_created']



class AssignedRefillOrderSerializer(serializers.ModelSerializer):
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
		fields = ['transaction_id', 'delivery_officer']



class RefillOrderDetailSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()
    user_address = serializers.SerializerMethodField()
    user_lga = serializers.SerializerMethodField()
    user_phone_number = serializers.SerializerMethodField()
    user_class = serializers.SerializerMethodField()
    auxiliary_full_name = serializers.SerializerMethodField()
    auxiliary_phone_number = serializers.SerializerMethodField()
    cylinder_type = serializers.SerializerMethodField()
    delivery_officer_fullname = serializers.SerializerMethodField()

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

    def get_user_lga(self, obj):
    	return obj.user.lga

    def get_delivery_officer_fullname(self, obj):
    	delivery_officer = obj.delivery_officer
    	return obj.delivery_officer.get_full_name() if delivery_officer else None

 

    class Meta:
        model = RefillOrder
        fields = ['id', 'user_full_name', 'user_address', 'user_lga', 'user_phone_number', 'user_class', 'smart_box', 'cylinder', 'cylinder_type', 
        	'order_id', 'status', 'access_code', 'transaction_id', 'delivery_officer_fullname', 'date_created', 'auxiliary_full_name', 'auxiliary_phone_number']



# Swap Bottle Serializers
class CylinderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cylinder
        fields = ['cylinder_serial_number', 'cylinder_total_weight']

class OtherBillableAssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherBillableAssets
        fields = ['low_pressure_regulator_price_per_yard', 'high_pressure_regulator_price_per_yard',
                  'low_pressure_hose_price_per_yard', 'high_pressure_hose_price_per_yard',
                  'subsidized_cylinder_price']

class RefillOrderSwapSerializer(serializers.ModelSerializer):
    #old_cylinder = CylinderSerializer()
    old_cylinder_serial_number = serializers.CharField(max_length=50)
    old_cylinder_total_weight = serializers.DecimalField(max_digits=10, decimal_places=2)
    new_cylinder = serializers.CharField(max_length=50)
    low_pressure_regulator_yards = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    high_pressure_regulator_yards = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    low_pressure_hose_yards = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    high_pressure_hose_yards = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    subsidized_cylinder_yards = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    def get_new_cylinder_serial_number(self, obj):
    	return obj.cylinder.cylinder_serial_number

    class Meta:
        model = RefillOrder
        fields = ['old_cylinder_serial_number', 'old_cylinder_total_weight', 'new_cylinder',
                  'low_pressure_regulator_yards', 'high_pressure_regulator_yards',
                  'low_pressure_hose_yards', 'high_pressure_hose_yards',
                  'subsidized_cylinder_yards']

    # def validate(self, data):
    #     # Get the old cylinder based on the serial number
    #     old_cylinder_serial_number = data.get('old_cylinder_serial_number')
    #     try:
    #         old_cylinder = Cylinder.objects.get(cylinder_serial_number=old_cylinder_serial_number)
    #     except Cylinder.DoesNotExist:
    #         raise serializers.ValidationError(f"Old cylinder with serial number '{old_cylinder_serial_number}' not found.")
        
    #     # Calculate the remnant
    #     tare_weight = old_cylinder.tare_weight
    #     total_weight = data.get('old_cylinder_total_weight')
    #     remnant = total_weight - tare_weight

    #     # Get the new cylinder based on the serial number
    #     new_cylinder_serial_number = data.get('new_cylinder')
    #     try:
    #         new_cylinder = Cylinder.objects.get(cylinder_serial_number=new_cylinder_serial_number)
    #     except Cylinder.DoesNotExist:
    #         raise serializers.ValidationError(f"New cylinder with serial number '{new_cylinder_serial_number}' not found.")
        
    #     # Calculate the quantity billable
    #     content_capacity = new_cylinder.capacity
    #     quantity_billable = content_capacity - remnant

    #     # Calculate the invoice
    #     gas_price = GasPrice.objects.latest('date_added').current_price
    #     invoice = gas_price * quantity_billable

    #     data['remnant'] = remnant
    #     data['quantity_billable'] = quantity_billable
    #     data['invoice'] = invoice

    #     return data

    # class Meta:
    #     model = RefillOrder
    #     fields = ['old_cylinder_serial_number', 'old_cylinder_total_weight', 'new_cylinder',
    #               'low_pressure_regulator_yards', 'high_pressure_regulator_yards',
    #               'low_pressure_hose_yards', 'high_pressure_hose_yards',
    #               'subsidized_cylinder_yards', 'remnant', 'quantity_billable', 'invoice']

    # def validate(self, attrs):
    #     old_cylinder = attrs.get('old_cylinder')
    #     new_cylinder_serial_number = attrs.get('new_cylinder_serial_number')

    #     # Check if the old cylinder exists
    #     if old_cylinder is None:
    #         raise serializers.ValidationError("Old cylinder details are required.")

    #     # Check if the new cylinder exists
    #     try:
    #         new_cylinder = Cylinder.objects.get(cylinder_serial_number=new_cylinder_serial_number)
    #         attrs['new_cylinder'] = new_cylinder
    #     except Cylinder.DoesNotExist:
    #         raise serializers.ValidationError("New cylinder does not exist.")

    #     return attrs

class BillableAssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherBillableAssets
        fields = ['low_pressure_regulator_yards', 'high_pressure_regulator_yards', 'low_pressure_hose_price_per_yard', \
        'high_pressure_hose_price_per_yard', 'subsidized_cylinder_price'] 


# class InvoiceBreakdownSerializer(serializers.ModelSerializer):
# 	billable_assets = BillableAssetsSerializer(source='billable_assets', read_only=True)
# 	quantity_billable_cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
# 	date_created = serializers.DateTimeField(source='invoice.date_created', read_only=True)

# 	def get_billable_assets(self, obj):
# 		return {
# 			'low_pressure_regulator': obj.low_pressure_regulator_yards,
# 			'high_pressure_regulator': obj.high_pressure_regulator_yards,
# 			'low_pressure_hose': obj.low_pressure_hose_yards,
# 			'high_pressure_hose': obj.high_pressure_hose_yards,
# 			'subsidized_cylinder_price': obj.subsidized_cylinder_yards,
# 		}

# 	class Meta:
# 		model = RefillOrder
# 		fields = ['billable_assets', 'quantity_billable_cost', 'date_created']


class InvoiceBreakdownSerializer(serializers.ModelSerializer):
    billable_assets = BillableAssetsSerializer(read_only=True)
    quantity_billable_cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    date_created = serializers.DateTimeField(source='invoice.date_created', read_only=True)

    class Meta:
        model = RefillOrder
        fields = ['billable_assets', 'quantity_billable_cost', 'date_created']


class Invoice1BreakdownSerializer(serializers.ModelSerializer):
    billable_assets = serializers.SerializerMethodField()
    quantity_billable_cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    date_created = serializers.DateTimeField(source='invoice.date_created', read_only=True)

    def get_billable_assets(self, obj):
        return {
            'low_pressure_regulator': obj.low_pressure_regulator_yards,
            'high_pressure_regulator': obj.high_pressure_regulator_yards,
            'low_pressure_hose': obj.low_pressure_hose_yards,
            'high_pressure_hose': obj.high_pressure_hose_yards,
            'subsidized_cylinder_price': obj.subsidized_cylinder_yards,
        }

    def get_quantity_billable_cost(self, obj):
        # Calculate quantity billable cost based on billable assets and gas quantity billable
        gas_price_per_kg = obj.gas_price.current_price
        quantity_billable = obj.new_cylinder.cylinder_capacity - obj.quantity_remaining
        billable_assets_cost = 0

        # Retrieve billable assets prices
        other_assets = OtherBillableAssets.objects.latest('date_added')

        if obj.low_pressure_regulator_yards:
            billable_assets_cost += other_assets.low_pressure_regulator_price_per_yard * obj.low_pressure_regulator_yards
        if obj.high_pressure_regulator_yards:
            billable_assets_cost += other_assets.high_pressure_regulator_price_per_yard * obj.high_pressure_regulator_yards
        if obj.low_pressure_hose_yards:
            billable_assets_cost += other_assets.low_pressure_hose_price_per_yard * obj.low_pressure_hose_yards
        if obj.high_pressure_hose_yards:
            billable_assets_cost += other_assets.high_pressure_hose_price_per_yard * obj.high_pressure_hose_yards
        if obj.subsidized_cylinder_yards:
            billable_assets_cost += other_assets.subsidized_cylinder_price * obj.subsidized_cylinder_yards

        quantity_billable_cost = gas_price_per_kg * quantity_billable + billable_assets_cost
        return quantity_billable_cost

    class Meta:
        model = RefillOrder
        fields = ['billable_assets', 'quantity_billable_cost', 'date_created']
