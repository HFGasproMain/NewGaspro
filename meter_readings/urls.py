from django.urls import path 
from .views import SmartBoxDefaultReadingsView, AssignedSmartBoxReadingsView, CreateActivatedSmartboxReadingView, ActivatedSmartBoxReadingsListView, \
	CollectGasReadingView, GasReadingHistoryAPIView, GasMeterStatusView, SmartBoxReadings, ResidentialUserMeterReadingsListView, \
	 ResidentialUserMeterReadingsHistoryAPIView, ResidentialUserMeterReadingSearchAPIView, UserGasConsumptionAndCostAPIView, UserDetailView, \
	 UserGasConsumptionAndCostSmartBoxAPIView

urlpatterns = [
	
	path('smartboxreadings/live-collect/', CollectGasReadingView.as_view(), name='smartbox-readings-collect'),
	#path('smartboxreadings/allreadings/', MeterReadingsListView.as_view(), name='smartbox-readings-list'),
	#path('smartboxreadings/user-readings/', UserGasReadingListView.as_view(), name='user-smartbox-readings'),
	#path('smartboxreadings/residential/', GasMeterStatusView.as_view(), name='user-smartbox-readings'),
	path('smartboxreadings/residential/', ResidentialUserMeterReadingsListView.as_view(), name='residential-meter-readings'),

	# alt
	#path('smartboxreadings/default/', SmartBoxReadings.as_view(), name='default-smartbox-readings'),

	
	# meter readings history
	path('smartboxreadings/history/<str:smart_box_id>/', ResidentialUserMeterReadingsHistoryAPIView.as_view(), name='smartbox-readings-history'),
	path('smartboxreadings/detail/<str:smart_box_id>/', GasReadingHistoryAPIView.as_view(), name='smartbox-readings-detail'),

	# meter_reading user_detail
	path('smartboxreadings/user-consumption/<int:user_id>/', UserGasConsumptionAndCostAPIView.as_view(), name='user_gas_consumption_and_cost'),
	path('smartboxreadings/usergas-consumption/<str:smart_box_id>/', UserGasConsumptionAndCostSmartBoxAPIView.as_view(), name='user_gas_consumption_and_cost'),
	path('smartboxreadings/user/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),

	# gas reading search
	path('smartboxreadings/search/', ResidentialUserMeterReadingSearchAPIView.as_view(), name='gas-readings-search'),


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