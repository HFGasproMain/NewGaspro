from rest_framework import serializers
from .models import Retailers 


class RetailersSerializer(serializers.ModelSerializer):
	class Meta:
		model = Retailers
		fields = ['business_name', 'business_email', 'business_address',
				'business_lga', 'business_state', 'business_phone_number', 'first_reference', 'second_reference']

# class RetailerSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()

#     class Meta:
#         model = Retailers
#         fields = ['business_name', 'business_address', 'business_lga', 'business_state', 'business_phone_number',
#                   'image', 'first_reference', 'second_reference', 'is_online', 'date_added', 'user']

#     def get_user(self, obj):
#         return obj.user.username

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['business_name'],
#             password='hf20231234'  # Set the default password here
#         )
#         validated_data['user'] = user
#         retailer = Retailers.objects.create(**validated_data)
#         return retailer



class RetailersUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Retailers
		fields = ['first_name', 'last_name', 'business_name', 'email', 'business_address',
				'business_lga', 'business_state', 'business_phone_number', 'first_reference', 'second_reference', 'is_online']


class RetailersListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Retailers
		fields = ['business_name', 'business_email', 'business_address', 'business_lga', 
			'business_state', 'business_phone_number', 'state_code', 'lga_code', 'first_reference', 'second_reference', 'is_online', 'date_added']