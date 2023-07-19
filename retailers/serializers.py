from rest_framework import serializers
from .models import Retailers, Manager
#from dateutil import parser


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
		fields = ['id', 'business_name', 'business_email', 'business_address', 'business_lga', 
			'business_state', 'business_phone_number', 'state_code', 'lga_code', 'first_reference', 'second_reference', 'is_online', 'date_added']



class CreateManagerSerializer(serializers.Serializer):
	GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
	retailer_id = serializers.PrimaryKeyRelatedField(queryset=Retailers.objects.all())
	first_name = serializers.CharField(max_length=50)
	last_name = serializers.CharField(max_length=50)
	mobile_number = serializers.CharField(max_length=11)
	gender = serializers.ChoiceField(choices=GENDER_CHOICES)
	dob = serializers.CharField()

	# def validate_dob(self, value):
	# 	try:
	# 		dob = parser.parse(value).date().strftime('%Y-%m-%d')
	# 	except (ValueError, AttributeError):
	# 		raise serializers.ValidationError('Invalid date format. Use YYYY-MM-DD format.')
	# 	return dob

class ROManagersListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Manager
		fields = '__all__'

