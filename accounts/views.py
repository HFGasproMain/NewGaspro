import datetime
import uuid

from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
#from django.utils.encoding import force_bytes, force_text
from django.utils.encoding import force_str, force_bytes

#from asset.models import Cylinder, AssignCylinder
#from asset.serializers import CylinderSerializer

from .serializers import SMEUserRegistrationSerializer, StaffUserRegistrationSerializer, AdminLoginSerializer, \
	UserLoginSerializer, UserListSerializer, UserSerializer, OpsDeliverySerializer, ResidentUserRegistrationSerializer, \
    SME2ListSerializer, UserUpdateSerializer, ResidentialUserSerializer, PasswordChangeSerializer, PasswordResetSerializer, \
    PasswordResetConfirmSerializer, DeviceTokenSerializer
    #InvestorSerializer, InvestorClientRequestSerializer, InvestorClientSerializer, InvestorInterestSerializer, \

from .models import User, SMEUser2
    
#from payment.models import MonthlyRent, Invoice
#from reading.models import Notification


# User Registrations Views
class SMEUserRegistrationView(APIView):
    serializer_class = SMEUserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        # if request.data.get('first_name') is None or request.data.get('last_name') is None: return Response({
        # "message": "First name or last name must be supplied"}, status=status.HTTP_400_BAD_REQUEST)
        # if request.data.get('business_name') is None or request.data.get('business_state') is None \
        #         or request.data.get('business_address') is None or request.data.get('business_type') is None:
        #     return Response({"message": "All business details must be supplied"}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('phone_number') is None:
            return Response({"message": "Phone number cannot be empty!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(phone_number=request.data.get('phone_number')).exists():
            return Response({"message": "User with this phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)

        business_phone_number = request.data.get('phone_number')
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        role = 1
        #generate_wallet_url = WALLET_URL + "wallet/generate"

        if valid:
            serializer.save()
            print(serializer.data)

            business_type = request.data.get('business_type')
            cylinder_size = request.data.get('cylinder_size')
            cylinder_size = str(cylinder_size) + ".00"

            # if business_type == "Business Pro":
            #     assignment = 1
                # rent_object = {
                #     "user_id": serializer.data['id'],
                #     "rent_amount": 400.0,
                #     "rent_status": "Pending",
                #     "rent_month": str(datetime.date.today().month),
                #     "rent_date": datetime.datetime.now()
                # }

                # MonthlyRent.objects.create(**rent_object)

            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'message': 'User successfully registered!',
                'sme_user_info': serializer.data
            }
            notification_payload = {
                "user": serializer.data['id'],
                "header": "Welcome home",
                "content": "Welcome to Homefort SME",
                "notif_type": "Blue",
                "date": datetime.datetime.today()
            }

            # Notification.objects.create(**notification_payload)

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "No user enabled to create questionnaire and wallet"},
                            status=status.HTTP_400_BAD_REQUEST)


class ResidentUserRegistrationView(APIView):
    serializer_class = ResidentUserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        #global assignment
        #the_referral = ''
        #referral_code = request.POST.get('any_referral_code')
        referral_code = request.data.get('any_referral_code')
        print(f'initial reffered_by => {referral_code}')

        if request.data.get('first_name') is None or request.data.get('last_name') is None:
            return Response({"message": "First name or last name must be provided!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('phone_number') is None:
            return Response({"message": "Phone number cannot be empty!"}, status=status.HTTP_400_BAD_REQUEST) 

        if request.data.get('email') is None:
            return Response({"message": "Email address cannot be empty!"}, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('email') is None:
            return Response({"message": "Email address cannot be empty!"}, status=status.HTTP_400_BAD_REQUEST) 

        if request.data.get('date_for_your_onboarding') is None:
            return Response({"message": "Please choose an onboarding date!"}, status=status.HTTP_400_BAD_REQUEST) 
        
        if User.objects.filter(phone_number=request.data.get('phone_number')).exists():
            return Response({"message": "User with this phone number already exists!"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=request.data.get('email')).exists():
            return Response({"message": "User with this email address already exists!"}, status=status.HTTP_400_BAD_REQUEST)

        if referral_code:
            # validate the credibility of the referral_code
            print('referral_code is given')
            try:
                the_referral = User.objects.filter(referral_code=request.data.get('any_referral_code')).first()
                # referral_code is valid
                if the_referral:
                    print(f'the REAL referral => {the_referral}')
                    role = 5
                    referred_by = the_referral
                    serializer = self.serializer_class(data=request.data)
                    valid = serializer.is_valid(raise_exception=True)

                    if valid:
                        serializer.save(role=role, referred_by=the_referral)
                        print(serializer.data)
                        response = {
                            'success': True,
                            'statusCode': status.HTTP_201_CREATED,
                            'message': 'User successfully registered!',
                            'user_info': serializer.data,
                            #'referral_code': user.referral_code
                        }
                        return Response(response, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"message": "User not created. Please review your details and try again!"},
                                        status=status.HTTP_400_BAD_REQUEST)
            except AttributeError:
                return Response({"message": "User with this referral code doesn't exists!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # No referral_code available
            print(f'the EMPTY referral')
            role = 5
            #referred_by = the_referral
            serializer = self.serializer_class(data=request.data)
            valid = serializer.is_valid(raise_exception=True)

            if valid:
                serializer.save(role=role)
                print(serializer.data)
                response = {
                    'success': True,
                    'statusCode': status.HTTP_201_CREATED,
                    'message': 'User successfully registered!',
                    'user_info': serializer.data,
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "User not created. Please review your details and try again!"},
                                status=status.HTTP_400_BAD_REQUEST)
    



class AdminUserRegistrationView(APIView):
    serializer_class = StaffUserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        if request.data.get('first_name') is None or request.data.get('last_name') is None:
            return Response({"message": "First name or last name must be supplied"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('phone_number') is None:
            return Response({"message": "Phone number cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('lga') is None or request.data.get('address') is None or request.data.get('state') is None:
               return Response({"message": "All address details must be provided!"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone_number=request.data.get('phone_number')).exists():
            return Response({"message": "User with this phone number already exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        role = 2

        if valid:
            serializer.save(role=role, user_class="Homefort Admin")

            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'message': 'Admin user successfully created!',
                'user_info': serializer.data
            }

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "No user enabled to create questionnaire and wallet"},
                            status=status.HTTP_400_BAD_REQUEST)


class DeliveryUserRegistrationView(APIView):
    serializer_class = StaffUserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        if request.data.get('first_name') is None or request.data.get('last_name') is None:
            return Response({"message": "First name or last name must be supplied"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('phone_number') is None:
            return Response({"message": "Phone number cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone_number=request.data.get('phone_number')).exists():
            return Response({"message": "User with this phone number already exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        role = 3

        if valid:
            serializer.save(role=role, user_class="Delivery Staff")
                            #bvn="0123456789")

            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'message': 'Delivery user successfully registered!',
                'user_info': serializer.data
            }

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "No user enabled to create questionnaire and wallet"},
                            status=status.HTTP_400_BAD_REQUEST)


class OperationsUserRegistrationView(APIView):
    serializer_class = StaffUserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        if request.data.get('first_name') is None or request.data.get('last_name') is None:
            return Response({"message": "First name or last name must be supplied"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('phone_number') is None:
            return Response({"message": "Phone number cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('lga') is None or request.data.get('address') is None or request.data.get('state') is None:
               return Response({"message": "All address details must be provided!"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone_number=request.data.get('phone_number')).exists():
            return Response({"message": "User with this phone number already exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        role = 4

        if valid:
            serializer.save(role=role, user_class="Operations Staff")

            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'message': 'Operations user successfully created!',
                'user_info': serializer.data
            }

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "No user enabled to create questionnaire and wallet"},
                            status=status.HTTP_400_BAD_REQUEST)


# User Login Views
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            if User.objects.filter(phone_number=request.data.get('phone_number')).exists():
                user = User.objects.get(phone_number=request.data.get('phone_number'))
                if request.data.get('phone_number') == user.phone_number and user.check_password(
                        request.data.get('password')):
                    response = {
                        'user_id': str(user.id),
                        'phone_number': serializer.data['phone_number'],
                        'success': True,
                        'statusCode': status.HTTP_200_OK,
                        'role': user.role,
                        'message': 'Login successful',
                        'access': serializer.data['access'],
                        'refresh': serializer.data['refresh']
                    }
                    return Response(response)
                else:
                    return Response({"message": "Invalid phone number or password entered"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Invalid phone number or password entered"},
                                status=status.HTTP_400_BAD_REQUEST)


class AdminLoginView(APIView):
    serializer_class = AdminLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            if User.objects.filter(email=request.data.get('email')).exists():
                user = User.objects.get(email=request.data.get('email'))

                if user.role != 2:
                    return Response({"message": "You are not authorised to view this page. Please contact admin!"},
                                    status=status.HTTP_400_BAD_REQUEST)

                if request.data.get('email') == user.email and user.check_password(
                        request.data.get('password')):
                    response = {
                        'user_id': str(user.id),
                        'email': user.email,
                        'success': True,
                        'statusCode': status.HTTP_200_OK,
                        'role': user.role,
                        'message': 'Login successful',
                        #'access': serializer.data['access'],
                        #'refresh': serializer.data['refresh']
                    }
                    return Response(response)
                else:
                    return Response({"message": "Invalid email or password entered"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Invalid email or password entered"},
                                status=status.HTTP_400_BAD_REQUEST)


# Get Users View
class UserListView(APIView):
    serializer_class = UserListSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class SMEUserListView(APIView):
# 	""" SME Customers List View """
# 	serializer_class = UserListSerializer
# 	permission_classes = (AllowAny,)

# 	def get(self, request):
# 		users = User.objects.filter(role=1)
# 		serializer = self.serializer_class(users, many=True)
# 		return Response(serializer.data, status=status.HTTP_200_OK)


class SMEUserListView(APIView):
    """ SME Customers List View """
    serializer_class = SME2ListSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        users = SMEUser2.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ResidentialUsersListView(APIView):
    """ All Residential Customers API """
    serializer_class = ResidentialUserSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        users = User.objects.filter(role=5)
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminUserListView(APIView):
	""" Admin List View """
	serializer_class = UserListSerializer
	permission_classes = (AllowAny,)
	
	def get(self, request):
	    users = User.objects.filter(role=2)
	    serializer = self.serializer_class(users, many=True)
	    return Response(serializer.data, status=status.HTTP_200_OK)


class DeliveryUserListView(APIView):
	""" Delivery List View """
	serializer_class = UserListSerializer
	permission_classes = (AllowAny,)

	def get(self, request):
		users = User.objects.filter(role=3)
		serializer = self.serializer_class(users, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

# Delivery & Ops Users
@api_view(['GET'])
@permission_classes((AllowAny,))
def get_ops_and_delivery(self):
	""" Returns a List of Operations & Delivery Staff """
	ops_list = list(User.objects.filter(role=4).values())
	delivery_list = list(User.objects.filter(role=3).values())
	total_list = ops_list + delivery_list
	return Response({"data": total_list,
                    "message": "Successfully returned a list of delivery & operations staff"},
                    status=status.HTTP_200_OK)

class OpsDeliveryListView(APIView):
	""" Returns a List of Operations & Delivery Staff """
	serializer_class = OpsDeliverySerializer
	permission_classes = (AllowAny,)

	def get(self, request):
		ops_users = list(User.objects.filter(role=4))
		delivery_users = list(User.objects.filter(role=3))
		combined_users = ops_users + delivery_users
		serializer = self.serializer_class(combined_users, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)



# User Profile View
@api_view(['GET'])
@permission_classes((AllowAny,))
def get_user_profile(self, user_id):
	""" User Profile View """
	try:
		user_profile = User.objects.get(id=user_id)
		serialized_user_profile = UserSerializer(user_profile)
		return Response({"message": "success", "data": serialized_user_profile.data}, status=status.HTTP_200_OK)
	except User.DoesNotExist:
		return Response({"message": "User does not exist. Please ensure they are registered!"},
			status=status.HTTP_400_BAD_REQUEST)



# Delete User
@api_view(['DELETE'])
@permission_classes((AllowAny,))
def delete_user(self, user_id):
    try:
        User.objects.get(id=user_id).delete()
        return Response({"message": "User has been deleted"}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response("This user does not exist on Homefort SME", status=status.HTTP_400_BAD_REQUEST)


# Update User
class UpdateUserProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        result = generics.get_object_or_404(self.queryset, id=self.kwargs["user_id"])
        return result

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)



# Password change
class PasswordChangeView(APIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully."})
        return Response(serializer.errors, status=400)


# Password reset
class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        current_site = get_current_site(request)
        mail_subject = 'Reset your password'
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
        })
        send_mail(mail_subject, message, 'from@example.com', [email])
        return Response({'detail': 'Password reset email has been sent.'})


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    
    def post(self, request, *args, **kwargs):
        uid = force_text(urlsafe_base64_decode(request.data.get('uid')))
        token = request.data.get('token')
        password = request.data.get('password')
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({'detail': 'Password has been reset successfully.'})
        else:
            return Response({'detail': 'Invalid token.'})


class DeviceTokenUpdateView(generics.UpdateAPIView):
    serializer_class = DeviceTokenSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def get_object(self):
        user_id = self.kwargs['id']
        return User.objects.get(user_id=user_id)