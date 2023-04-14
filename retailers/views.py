from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import Retailers
from accounts.pagination import LargeResultsSetPagination
from .serializers import RetailersSerializer, RetailersUpdateSerializer, RetailersListSerializer
from .permissions import IsAdminOrReadOnly


# Create your views here.
class RetailersCreateView(generics.CreateAPIView):
	""" Create a Retailer """
	queryset = Retailers.objects.all()
	serializer_class = RetailersSerializer
	permission_classes = (IsAdminOrReadOnly, permissions.IsAuthenticated)


class RetailersListView(generics.ListAPIView):
	""" All Established Retailers """
	queryset = Retailers.objects.all()
	serializer_class = RetailersListSerializer
	permission_classes = (AllowAny,)
	pagination_class = LargeResultsSetPagination



class RetailersDetailView(generics.RetrieveUpdateDestroyAPIView):
	"""  Retailers Update & Delete API Accessible to Admins Only """
	permission_classes = (IsAdminOrReadOnly,)
	#permission_classes = (AllowAny,)
	queryset = Retailers.objects.all()
	serializer_class = RetailersSerializer
	
	

