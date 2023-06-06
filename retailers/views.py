from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


from .models import Retailers
from accounts.pagination import LargeResultsSetPagination
from .serializers import RetailersSerializer, RetailersUpdateSerializer, RetailersListSerializer
from .permissions import IsAdminOrReadOnly

from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
class RetailersCreateView(generics.CreateAPIView):
	""" Create a Retailer """
	queryset = Retailers.objects.all()
	serializer_class = RetailersSerializer
	#lpermission_classes = (IsAdminOrReadOnly, permissions.IsAuthenticated)

	# def perform_create(self, serializer):
    #     user = User.objects.create_user(
    #         username=self.request.data['business_name'],
    #         password='hf20231234'  # Set the default password here
    #     )
    #     serializer.save(user=user)

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
	
	

class CreateManagerAPIView(APIView):
    def post(self, request):
        # Extract the required data from the request
        retailer_id = request.data.get('retailer_id')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        gender = request.data.get('gender')
        dob = request.data.get('dob')

        # Retrieve the retailer (ro) instance
        retailer = Retailers.objects.get(id=retailer_id)

        # Create the user instance with the default password
        default_password = 'hf20231234'
        user = User.objects.create_user(username='homefort_manager_username', password=default_password)

        # Create the manager and associate it with the retailer
        manager = Manager.objects.create(user=user, retailer=retailer, first_name=first_name, last_name=last_name, gender=gender, dob=dob)

        # Return a success response without including the default password
        return Response({'status': 'success', 'message': 'Manager created successfully'}, status=status.HTTP_201_CREATED)

    
