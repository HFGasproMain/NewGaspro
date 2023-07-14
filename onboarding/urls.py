from django.urls import path
from .views import ResidentialPendingOnboardingListView

urlpatterns = [
	path('pending-users/', ResidentialPendingOnboardingListView.as_view(), name='pending-onboarding'),
]