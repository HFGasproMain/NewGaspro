from django.urls import path
from .views import OnboardedOrderBillingListView

urlpatterns = [
	path('onboarded-orders/', OnboardedOrderBillingListView.as_view(), name='onboard-billing'),
]
