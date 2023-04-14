from django.urls import path
from .views import OnboardingOrderCreateView, OnboardedOrderListView

urlpatterns = [
	path('onboard-order/', OnboardingOrderCreateView.as_view(), name='onboard-order'),
	path('onboarded-orders/', OnboardedOrderListView.as_view(), name='list-onboard-order')
]