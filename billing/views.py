from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import OrderOnboardBilling
from .serializers import OnboardOrderSerializer

# Create your views here.
class OnboardedOrderBillingListView(generics.ListAPIView):
	""" API To List All Onboarded Customer Orders """
	queryset = OrderOnboardBilling.objects.all()
	#my_values = queryset.values('customer', 'order', '')
	serializer_class = OnboardOrderSerializer
			