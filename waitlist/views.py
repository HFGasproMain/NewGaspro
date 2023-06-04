from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import Waitlist
from .serializers import WaitlistSerializer
from orders.pagination import LargeResultsSetPagination

# Create your views here.
class WaitlistCreateView(generics.CreateAPIView):
	""" API For Registered Users Who Wanna Be On The Waitlist  """
	queryset = Waitlist.objects.all()
	serializer_class = WaitlistSerializer
	permission_classes = (AllowAny,)


class WaitlistListView(APIView):
	""" API For Users Waitlist """
	pagination_class = LargeResultsSetPagination
	def get(self, request):
		users_waitlist = Waitlist.objects.all()

		# Create an instance of the pagination class
		paginator = self.pagination_class()

		# Paginate the queryset
		paginated_users_waitlist = paginator.paginate_queryset(users_waitlist, request)

		# Serialize the paginated results
		serializer = WaitlistSerializer(paginated_users_waitlist, many=True)

		# Return the paginated response
		return paginator.get_paginated_response(serializer.data) 



		

