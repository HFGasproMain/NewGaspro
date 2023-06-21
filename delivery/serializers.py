from rest_framework import serializers
from .models import DeliveryOfficer


class DeliveryOfficerSerializer(serializers.ModelSerializer):
	retail_outlet_business_name = serializers.SerializerMethodField()
	retail_outlet_lga = serializers.SerializerMethodField()
	
	class Meta:
		model = DeliveryOfficer
		#fields = '__all__'
		fields = ['id', 'manager', 'retail_outlet_business_name', 'retail_outlet_lga', 'first_name', 'last_name', 'do_phone_number', 'gender', 
		'nok_first_name', 'nok_last_name', 'nok_phone_number', 'nok_relationship', 'date_created']

	def get_retail_outlet_business_name(self, obj):
		return f"{obj.manager.business_name}"


	def get_retail_outlet_lga(self, obj):
		return f"{obj.manager.business_lga}"
		