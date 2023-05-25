from django.urls import path
from .views import CylinderCreateView, CylinderListView, CylinderDeleteView, CylinderUpdateView, SMEAssignedCylinderListView, \
	SmartScaleCreateView, SmartScaleListView, SmartScaleDeleteView, SmartScaleUpdateView, SmartBoxCreateView, \
	 SmartBoxDeleteView, SmartBoxUpdateView, SmartBoxListView, SMEAssignCylinderCreateView, ResidentialAssignedCylinderListView, \
     SMEUserAssignedCylinderHistory, AssignedCylinderHistory, ResidentialAssignCylinderCreateView, CylinderDetailView, \
     cylinder_detail_view, OtherBillableAssetsCreateView, GasPriceCreateView, OtherBillableAssetsListView, GasPriceListView, \
     OtherBillableAssetsUpdateView, GasPriceUpdateView

urlpatterns = [
	# assets create
	path("cylinder-create/", CylinderCreateView.as_view(), name='cylinder-create'),
    path("smartscale-create/", SmartScaleCreateView.as_view(), name='smartscale-create'),
    path("smartbox-create/", SmartBoxCreateView.as_view(), name='smartbox-create'),

    # assign cylinder
    path('sme/cylinder-onboard/', SMEAssignCylinderCreateView.as_view(), name='cylinder-onboard'),
    path('residential/cylinder-onboard/', ResidentialAssignCylinderCreateView.as_view(), name='residential-cylinder-onboard'),

    # assets list
    path("cylinders/", CylinderListView.as_view(), name='cylinders'),
    path("smartscales/", SmartScaleListView.as_view(), name='smartscales'),
    path("smartboxes/", SmartBoxListView.as_view(), name='smartboxes'),
    path("residential/assigned-cylinders/", ResidentialAssignedCylinderListView.as_view(), name='retailed-assigned-cylinders'),
    path("assigned-cylinders/sme/", SMEAssignedCylinderListView.as_view(), name='sme-assigned-cylinders'),
    path("history/assigned-cylinders/<str:sme_id>/", SMEUserAssignedCylinderHistory.as_view(), name='assignedcy-history-by-sme'),
    path("history/assigned-cylinder/<str:cy_tag_id>/", AssignedCylinderHistory.as_view(), name='assignedcy-history-by-cy'),

    # other asset prices
    path("gas-price-create/", GasPriceCreateView.as_view(), name='create-gas-price'),
    path("gas-price/", GasPriceListView.as_view(), name='gas-price'),
    path("update-gas-price/<str:pk>/", GasPriceUpdateView.as_view(), name='update-gas-price'),
    path("other-assets-create/", OtherBillableAssetsCreateView.as_view(), name='create-other-assets-price'),
    path("other-assets/", OtherBillableAssetsListView.as_view(), name='other-assets-price'),
    path("update-other-assets/<str:pk>/", OtherBillableAssetsUpdateView.as_view(), name='update-other-assets-price'),

    # single asset
    path("delete-smartscale/<str:pk>", SmartScaleDeleteView.as_view(), name='delete-smartscale'),
    path("update-smartscale/<str:pk>", SmartScaleUpdateView.as_view(), name='update-smartscale'),
    #path("cylinder/<str:pk>", CylinderDetailView.as_view(), name='cylinder-detail'), 
    path("cylinder/<str:cylinder>/", cylinder_detail_view, name='cylinder-detail'), 
    path("update-cylinder/<str:pk>/", CylinderUpdateView.as_view(), name='update-cylinder'),
    path("delete-cylinder/<str:pk>/", CylinderDeleteView.as_view(), name='delete-cylinder'),
    path("delete-smartbox/<str:pk>", SmartBoxDeleteView.as_view(), name='delete-smartbox'),
    path("update-smartbox/<str:pk>", SmartBoxUpdateView.as_view(), name='update-smartbox'),
]
