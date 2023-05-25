from django.urls import path 
from .views import SmartBoxDefaultReadingsView, AssignedSmartBoxReadingsView, CreateActivatedSmartboxReadingView, \
	ActivatedSmartBoxReadingsListView, CollectGasReadingView

urlpatterns = [
	
	path('smartboxreadings/live-collect/', CollectGasReadingView.as_view(), name='smartbox-readings-collect'),
	path('smartboxreadings/create/', CreateActivatedSmartboxReadingView.as_view(), name='smartbox-readings-create'),
	path('smartboxreadings/activated/', ActivatedSmartBoxReadingsListView.as_view(), name='activated-smartbox-readings'),

	path('smartboxreadings/default/', SmartBoxDefaultReadingsView.as_view(), name='smartbox-readings'),
	path('smartboxreadings/assigned/', AssignedSmartBoxReadingsView.as_view(), name='assignedsmartbox-readings'),

]


'''

- After creating assets, they're by default unassigned. 
- During onboarding, users can either approve order or reschedule
- After approval, DO onboards unassigned cylinders/smart device to users
- Payment is made and card is debited based on the generated invoice
- Smart device sends user gas readings to the server (post)
- When gas reading reach 2.0 kg, a refill trigger is automatically generated.
- Gas reading is done every 0.5kg ...
- Notification pops up to HQ, user and RO.
- RO assign DO for refill after user approves refill date.  

'''