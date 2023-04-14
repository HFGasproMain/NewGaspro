from rest_framework import serializers
from .models import Retailers 


class RetailersSerializer(serializers.ModelSerializer):
	class Meta:
		model = Retailers
		fields = ['first_name', 'last_name', 'business_name', 'email', 'business_address',
				'business_lga', 'business_state', 'business_phone_number', 'first_reference', 'second_reference']



class RetailersUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Retailers
		fields = ['first_name', 'last_name', 'business_name', 'email', 'business_address',
				'business_lga', 'business_state', 'business_phone_number', 'first_reference', 'second_reference', 'is_online']


class RetailersListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Retailers
		fields = ['first_name', 'last_name', 'business_name', 'email', 'business_address', 'business_lga', 
			'business_state', 'business_phone_number', 'first_reference', 'second_reference', 'is_online', 'date_added']