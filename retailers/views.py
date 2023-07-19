from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from datetime import datetime

from .models import Retailers, Manager
from accounts.pagination import LargeResultsSetPagination
from .serializers import RetailersSerializer, RetailersUpdateSerializer, RetailersListSerializer, CreateManagerSerializer, \
	ROManagersListSerializer
from .permissions import IsAdminOrReadOnly
from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()
current_date = datetime.today()


# Create your views here.
class RetailersCreateView(generics.CreateAPIView):
	""" API to Create a Retailer Outlet """
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
	
	

class CreateManagerAPIView(generics.CreateAPIView):
    """ API to Create a RO Manager """
    serializer_class = CreateManagerSerializer

    def post(self, request):
        # Extract the required data from the request
        retailer_id = request.data.get('retailer_id')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        mobile_number = request.data.get('mobile_number')
        gender = request.data.get('gender')
        dob = request.data.get('dob')

        # Validate required data
        if not retailer_id or not first_name or not last_name or not gender or not dob:
            return Response({'status': 'error', 'message': 'Incomplete data provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the retailer instance
            retailer = Retailers.objects.get(id=retailer_id)
        except Retailers.DoesNotExist:
            return Response({'status': 'error', 'message': 'Retailer not found.'}, status=status.HTTP_404_NOT_FOUND)


        # Create the user instance with the default password
        default_password = 'hf20231234'
        user = User.objects.create_user(date_for_your_onboarding=current_date, phone_number=mobile_number, password=default_password)

        # Create the manager and associate it with the retailer
        manager = Manager.objects.create(user=user, retailer=retailer, first_name=first_name, last_name=last_name, gender=gender, dob=dob)

        # Return a success response without including the default password
        return Response({'status': 'success', 'message': 'Manager created successfully'}, status=status.HTTP_201_CREATED)
    

class ROManagerListView(generics.ListAPIView):
	""" All Established Retailers """
	queryset = Manager.objects.all()
	serializer_class = ROManagersListSerializer
	permission_classes = (AllowAny,)
	pagination_class = LargeResultsSetPagination



def get_retailer_address(request, retailer_id):
    try:
        retailer = Retailers.objects.get(id=retailer_id)
        address = retailer.business_address
        lga = retailer.business_lga
        location = f'{address,lga}'
        return JsonResponse({'address': lga})
    except Retailers.DoesNotExist:
        return JsonResponse({'error': 'Retailer not found'}, status=404)

def get_retailer_code(request, retailer_id):
    try:
        retailer = Retailers.objects.get(id=retailer_id)
        code = retailer.get_retailers_code()
        return JsonResponse({'code': code})
    except Retailers.DoesNotExist:
        return JsonResponse({'error': 'Retailer not found'}, status=404)
