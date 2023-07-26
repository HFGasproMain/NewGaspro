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


class DeliveryOfficerProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    next_of_kin_full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_next_of_kin_full_name(self, obj):
        return f"{obj.nok_first_name} {obj.nok_last_name}"

    class Meta:
        model = DeliveryOfficer
        fields = ['full_name', 'date_created', 'unique_code', 'do_phone_number', 'next_of_kin_full_name',
         'nok_relationship', 'nok_phone_number']