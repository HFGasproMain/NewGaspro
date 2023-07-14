from accounts.models import User
from rest_framework import serializers





class PendingOnboardingSerializer(serializers.ModelSerializer):
	user_full_name = serializers.SerializerMethodField()
	user_full_address = serializers.SerializerMethodField()
	#user_lga = serializers.SerializerMethodField()
	user_phone_number = serializers.SerializerMethodField()
	user_scheduling_date = serializers.SerializerMethodField()

	def get_user_full_name(self, obj):
		return obj.get_full_name()

	def get_user_full_address(self, obj):
		return (obj.address, obj.lga)

	# def get_user_lga(self, obj):
	# 	return obj.lga  

	def get_user_phone_number(self, obj):
		return obj.phone_number 

	def get_user_scheduling_date(self, obj):
		return obj.date_for_your_onboarding

	class Meta:
		model = User
		fields = ['user_full_name', 'user_full_address', 'user_phone_number', 'user_scheduling_date']

