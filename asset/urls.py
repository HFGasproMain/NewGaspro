from django.urls import path
from .views import CylinderCreateView, CylinderListView, CylinderDeleteView, CylinderUpdateView, SMEAssignedCylinderListView, \
	SmartScaleCreateView, SmartScaleListView, SmartScaleDeleteView, SmartScaleUpdateView, SmartBoxCreateView, \
	 SmartBoxDeleteView, SmartBoxUpdateView, SmartBoxListView, SMEAssignCylinderCreateView, RetailAssignedCylinderListView, \
     SMEUserAssignedCylinderHistory, AssignedCylinderHistory, RetailAssignCylinderCreateView, CylinderDetailView, \
     cylinder_detail_view

urlpatterns = [
	# assets create
	path("cylinder-create/", CylinderCreateView.as_view(), name='cylinder-create'),
    path("smartscale-create/", SmartScaleCreateView.as_view(), name='smartscale-create'),
    path("smartbox-create/", SmartBoxCreateView.as_view(), name='smartbox-create'),

    # assign cylinder
    path('cylinder-onboard/sme/', SMEAssignCylinderCreateView.as_view(), name='cylinder-onboard'),
    path('cylinder-onboard/retail/', RetailAssignCylinderCreateView.as_view(), name='retail-cylinder-onboard'),

    # assets list
    path("cylinders/", CylinderListView.as_view(), name='cylinders'),
    path("smartscales/", SmartScaleListView.as_view(), name='smartscales'),
    path("smartboxes/", SmartBoxListView.as_view(), name='smartboxes'),
    path("assigned-cylinders/retail/", RetailAssignedCylinderListView.as_view(), name='retailed-assigned-cylinders'),
    path("assigned-cylinders/sme/", SMEAssignedCylinderListView.as_view(), name='sme-assigned-cylinders'),
    path("history/assigned-cylinders/<str:sme_id>/", SMEUserAssignedCylinderHistory.as_view(), name='assignedcy-history-by-sme'),
    path("history/assigned-cylinder/<str:cy_tag_id>/", AssignedCylinderHistory.as_view(), name='assignedcy-history-by-cy'),

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