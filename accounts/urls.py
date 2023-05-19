from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import (
    SMEUserRegistrationView, AdminUserRegistrationView, DeliveryUserRegistrationView, OperationsUserRegistrationView, 
    UserLoginView, UserListView, get_user_profile, AdminLoginView, get_ops_and_delivery, SMEUserListView, ResidentUserRegistrationView,
    AdminUserListView, DeliveryUserListView, UpdateUserProfileView, delete_user, OpsDeliveryListView, ResidentialUsersListView
)

urlpatterns =[
	# Registration
	path('sme/register/', SMEUserRegistrationView.as_view(), name='sme-register'),
    path('residential/register/', ResidentUserRegistrationView.as_view(), name='retail-register'),
    path('admin-register/', AdminUserRegistrationView.as_view(), name='admin-register'),
    path('delivery-register/', DeliveryUserRegistrationView.as_view(), name='delivery-register'),
    path('operations-register/', OperationsUserRegistrationView.as_view(), name='ops-register'),

    # Login
    path('login/', UserLoginView.as_view(), name='login'),
    path('admin/login', AdminLoginView.as_view(), name='admin-login'),

    # Users
    path('users/', UserListView.as_view(), name='users'),
    path('sme/clients/', SMEUserListView.as_view(), name='sme-users'),
    path('residential/users/', ResidentialUsersListView.as_view(), name='residential-users'),
    path('admin-users/', AdminUserListView.as_view(), name='users'),
    path('delivery-users/', DeliveryUserListView.as_view(), name='users'),
    #path('ops-delivery/', get_ops_and_delivery, name='ops-delivery'),
    path('ops-delivery/', OpsDeliveryListView.as_view(), name='ops-delivery'),
    
    # Single User
    path("user-profile/<str:user_id>", get_user_profile, name='user-profile'),
    path("update-profile/<str:user_id>", UpdateUserProfileView.as_view(), name='update-user'),
    path('delete-user/<str:user_id>', delete_user, name='delete-user'),

    #jwt
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
]

# {
# 	# for me
#     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NzU5Mjg3MiwiaWF0IjoxNjc3NTA2NDcyLCJqdGkiOiI5Y2I5NjMzOGUwYjA0MWE1YTI0NDgzZmM4NTZlZDg1YiIsInVzZXJfaWQiOjJ9.sJqP9a6ZOBxdBS6_LUhZl9Kb4mtLn86h2plJH1CxLSE",
#     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc3NTA2NzcyLCJpYXQiOjE2Nzc1MDY0NzIsImp0aSI6IjBjNzA2ODY1NzE4ZDQyOWRiOTliNmY0YWIwNDhmYTk4IiwidXNlcl9pZCI6Mn0.vztUme2_-dr_BBDPiZot4layqJKL9zntwTImutMmSGs"
# }