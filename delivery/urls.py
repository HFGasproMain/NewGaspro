from django.urls import path
#from .views import OnboardedOrderBillingListView
from .views import DeliveryOfficerCreateAPIView, DeliveryOfficerListAPIView, DeliveryOfficerOrdersListAPIView, DeliveryOfficerProfileView

urlpatterns = [
	path('create-officer/', DeliveryOfficerCreateAPIView.as_view(), name='create-do'),	
	path('all-officers/', DeliveryOfficerListAPIView.as_view(), name='list-do'),
	path('<int:pk>/officer-orders/', DeliveryOfficerOrdersListAPIView.as_view(), name='do-orders'),
	path('officer/<int:pk>/', DeliveryOfficerProfileView.as_view(), name='delivery-officer-retrieve'),
]
