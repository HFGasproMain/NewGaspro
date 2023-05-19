from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction

from .models import User, SMEUser2

# Registration Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'address', 'lga', 'state']


class ResidentialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email',  "referral_code", \
        'date_for_your_onboarding', 'date_joined', 'referred_by']


class SMEUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        model = SMEUser2
        fields = [
            'id',
            #'user',
            #'first_name',
            #'last_name',
            'phone_number',
            'email',
            'business_name',
            'business_address',
            'lga',
            'business_state',
            'business_type',
            'has_new_shop',
            'asset_type',
            'has_cylinder',
            'cylinder_size',
            'cylinder_position',
            'password',
            "token"
        ]    

    def create(self, validated_data):
        auth_user = SMEUser2.objects.create(**validated_data)
        return auth_user


class ResidentUserRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.SlugField(read_only=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    date_for_your_onboarding = serializers.DateField()
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'date_for_your_onboarding',
            #'lga',
            #'address',
            #'state',
            'password',
            'any_referral_code',
            "token",
        )

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user


class StaffUserRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.SlugField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'phone_number',
            'email',
            'first_name',
            'last_name',
            'lga',
            'address',
            'state',
            'password'
        )

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user


# Login Serializers
class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=128, write_only=False)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self, data):
        phone_number = data['phone_number']
        password = data['password']
        user = authenticate(phone_number=phone_number, password=password)

        # if user is None:
        #     raise serializers.ValidationError("Invalid login credentials")

        try:
            if not user is None:
                refresh = RefreshToken.for_user(user)
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)

                update_last_login(None, user)

                validation = {
                    'access': access_token,
                    'refresh': refresh_token,
                    'phone_number': user.phone_number,
                    'role': user.role,
                }
                return validation
            else:
                no_validation = {
                    'access': None,
                    'refresh': None,
                    'phone_number': None,
                    'role': None,
                }
                return no_validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=128, write_only=False)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self, data):
        password = data['password']
        user_email = data['email'] 
        user = authenticate(email=user_email, password=password)
        print('thisuser=>',user)

        try:
            if not user is None:
                refresh = RefreshToken.for_user(user)
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)

                update_last_login(None, user)

                validation = {
                    'access': access_token,
                    'refresh': refresh_token,
                    'phone_number': user.phone_number,
                    'role': user.role,
                }
                return validation
            else:
                no_validation = {
                    'access': None,
                    'refresh': None,
                    'phone_number': None,
                    'role': None,
                }
                return no_validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


# User Types Specials
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'last_login', 'is_superuser', 'password')

class OpsDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'last_login', 'is_superuser', 'password')

# Get Users
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'last_login', 'is_superuser', 'password')


class SME2ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMEUser2
        exclude = ('groups', 'user_permissions', 'last_login', 'is_superuser', 'password')


