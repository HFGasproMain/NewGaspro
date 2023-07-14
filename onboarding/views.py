from django.shortcuts import render
from accounts.models import User
from accounts.serializers import UserSerializer
from .serializers import PendingOnboardingSerializer
from meter_readings.pagination import MeterReadingsPagination

from rest_framework import generics
from rest_framework.permissions import AllowAny

# Create your views here.
class ResidentialPendingOnboardingListView(generics.ListAPIView):
	""" All Residential Users Pending Onboarding API """
	queryset = User.objects.all()
	serializer_class = PendingOnboardingSerializer
	permission_classes = (AllowAny,)
	pagination_class = MeterReadingsPagination

