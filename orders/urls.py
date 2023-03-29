from django.urls import path
from .views import OnboardingOrderCreateView, OnboardingOrderListView

urlpatterns = [
	path('onboard-order/', OnboardingOrderCreateView.as_view(), name='onboard-order'),
	path('onboarded-orders/', OnboardingOrderListView.as_view(), name='list-onboard-order')
]