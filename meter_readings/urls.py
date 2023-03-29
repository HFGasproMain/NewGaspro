from django.urls import path 
from .views import SmartBoxDefaultReadingsView, AssignedSmartBoxReadingsView

urlpatterns = [
	path('smartboxreadings/default/', SmartBoxDefaultReadingsView.as_view(), name='smartbox-readings'),
	path('smartboxreadings/assigned/', AssignedSmartBoxReadingsView.as_view(), name='assignedsmartbox-readings'),

]
