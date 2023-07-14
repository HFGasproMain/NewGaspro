from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()

    class Meta:
        model = Card
        fields = ['card_number', 'expiration_date', 'cvv', 'user_full_name', 'user']
