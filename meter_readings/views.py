import datetime
import uuid
import requests

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from asset.models import ResidentialAssignCylinder, Cylinder, SmartBox
from wallet.models import Wallet
from orders.models import OnboardingOrder
from .models import SmartBoxReadings, Range, ActivatedSmartBoxReading, CollectGasReading, GasMeterStatus
from .serializers import SmartBoxReadingsSerializer, RangeSerializer, AssignedSmartBoxReadingsSerializer, \
 ActivatedSmartboxReadingSerializer, CollectGasReadingsSerializer, ResidentialCustomersGasReadingsSerializer, \
 UserGasReadingSerializer, GasMeterStatusSerializer, UserGasMeterStatusSerializer

from decimal import Decimal
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum, Q
from django.http import JsonResponse

from .pagination import MeterReadingsPagination
User = get_user_model()

# All Views Here
class CollectGasReadingView(generics.CreateAPIView):
    """ API to Get Live SmartBox Readings From SmartBox Hardware/Device """
    queryset = CollectGasReading.objects.all()
    serializer_class = CollectGasReadingsSerializer

    def post(self, request, *args, **kwargs):
        serializer = SmartBoxReadingsSerializer(data=request.data)
        if serializer.is_valid():
            which_smart_box = request.data.get('smart_box_id')
            print(f'smart_box_id_received_from hardware => {which_smart_box}')
            qty_used = request.data.get('quantity_used')
            battery_remaining = request.data.get('battery_remaining')
            longitude = request.data.get('longitude')
            latitude = request.data.get('latitude')

            # Perform all calculations
            if ResidentialAssignCylinder.objects.filter(smart_box=which_smart_box).exists():
                print('Loading ...! SmartBox Exists!! ... Gas Reading Activated!!!')
                assigned_meter = ResidentialAssignCylinder.objects.filter(smart_box=which_smart_box).first()
    
                # Get the associated cylinder data
                user = assigned_meter.user
                print(f'user_id => {user}')
                cylinder = assigned_meter.cylinder
                qty_used = Decimal(qty_used)
                print(f'{qty_used},', type(qty_used))
                qty_supplied = assigned_meter.cylinder.cylinder_gas_content
                print(f'{qty_supplied},', type(qty_supplied))

                # Calculate the current cylinder_gas_quantity 
                qty_gas_left = qty_supplied - qty_used

                # Update the cylinder_gas_quantity in the Cylinder model
                cylinder.cylinder_gas_content = qty_gas_left
                cylinder.save()

                # keep for response usage
                new_cylinder_gas_quantity = cylinder.cylinder_gas_content
                serializer.save()

                # response_data = {
                # 'user_id': user.id,
                # 'full_name': [user.first_name, user.last_name],
                # #'last_name': user.last_name,
                # 'smart_box': which_smart_box,
                # 'battery_remaining': battery_remaining,
                # 'cylinder_serial_number': cylinder.cylinder_serial_number,
                # 'quantity_supplied': qty_supplied,
                # 'quantity_used':qty_used,
                # 'quantity_gas_left': new_cylinder_gas_quantity,
                # 'last_push': serializer.instance.last_push.strftime('%Y-%m-%d %H:%M:%S')
                # }
                response_data = {
                'user_id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'smart_box': which_smart_box,
                'battery_remaining': battery_remaining,
                'cylinder_serial_number': cylinder.cylinder_serial_number,
                'quantity_supplied': qty_supplied,
                'quantity_used':qty_used,
                'quantity_gas_left': new_cylinder_gas_quantity,
                'last_push': serializer.instance.last_push.strftime('%Y-%m-%d %H:%M:%S')
                }

                # Save gas status 
                GasMeterStatus.objects.create(**response_data)
                return Response({"message": "success", "data": response_data}, status=status.HTTP_200_OK)
            return Response({"message": "Cylinder not found!"}, status=status.HTTP_400_BAD_REQUEST)



class GasMeterStatusView(APIView):
    def get(self, request):
        # Retrieve all CollectGasReading instances
        gas_readings = CollectGasReading.objects.all()

        # Prepare response data
        response_data = []
        for gas_reading in gas_readings:
            smart_meter_id = gas_reading.smart_box_id
            print(f'assigned_meters => {smart_meter_id},')
            
            owner = ResidentialAssignCylinder.objects.filter(smart_box=smart_meter_id).last()
            gas_quantity_remaining = gas_reading.quantity_remaining

            # Append data to the response list
            response_data.append({
                'smart_meter_id': smart_meter_id,
                'first_name': owner.user.first_name,
                'last_name': owner.user.last_name,
                'gas_quantity_remaining': gas_quantity_remaining,
            })

        return Response(response_data)


class ResidentialUserMeterReadingsListView(generics.ListAPIView):
    """ API For Residential Customers Gas Readings """
    queryset = GasMeterStatus.objects.all()
    serializer_class = UserGasMeterStatusSerializer
    pagination_class = MeterReadingsPagination



class ResidentialUserMeterReadingSearchAPIView(generics.ListAPIView):
    """API to Search Gas Reading Details by Customer Name or Phone number"""
    serializer_class = GasMeterStatusSerializer
    pagination_class = MeterReadingsPagination

    def get_queryset(self):
        query = self.request.query_params.get('query')
        queryset = GasMeterStatus.objects.all()
        paginator = self.pagination_class()

        if query:
            # Filter gas readings by customer name
            queryset = queryset.filter(user_id__in=User.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(phone_number=query)).values('id'))

        paginated_queryset = paginator.paginate_queryset(queryset, self.request)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        #queryset =  GasMeterStatus.objects.all()
        paginator = self.pagination_class()
        
        if not queryset.exists():
            return Response({"message": "No gas meter readings found for this user!"}, status=status.HTTP_404_NOT_FOUND)
        
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        return paginator.get_paginated_response(serializer.data)


class UserDetailView(APIView):
    """ API For Residential User Detail """
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        # Assuming you have a UserProfile model that extends the User model
        phone_number = user.phone_number

        # Get the SmartBox object for the user
        smart_box = ResidentialAssignCylinder.objects.filter(user=user).first()
        smart_box_id = smart_box.smart_box_id if smart_box else None

        # Get the onboarding order for the user
        onboarding_order = OnboardingOrder.objects.filter(customer=user).first()
        date_of_onboarding = onboarding_order.date_created if onboarding_order else None

        data = {
            'full_name': user.get_full_name(),
            'address': user.get_full_address(),
            'phone_number': phone_number,
            'smart_box_id': smart_box_id,
            'date_of_onboarding': date_of_onboarding
        }

        return Response(data)


class ResidentialUserMeterReadingsHistoryAPIView(generics.RetrieveAPIView):
    """ API For Residential User Details (Gas Usage History & Invoice History)"""
    serializer_class = GasMeterStatusSerializer

    def get_object(self):
        meter_id = self.kwargs['smart_box_id']  
        #name = self.kwargs['name']
        
        # Check if the meter_id exists
        if not SmartBox.objects.filter(box_id=meter_id).exists():
            return None
        
        #queryset = CollectGasReading.objects.filter(residential_assign_meter__smart_meter_id=meter_id)
        queryset = GasMeterStatus.objects.filter(smart_box=meter_id)
        total_gas_used = queryset.aggregate(total_gas_used=Sum('quantity_used'))['total_gas_used']
        total_quantity_purchased = queryset.aggregate(total_quantity_purchased=Sum('quantity_supplied'))['total_quantity_purchased']

        # Calculate the total transactional amount based on other bills (e.g., onboarding bill, cylinder refill, etc.)
        # Replace 'other_bills' with the actual model representing other bills
        #total_transactional_amount = other_bills.objects.filter(user__smart_box=meter_id).aggregate(total_amount=Sum('amount'))['total_amount']

        # if name:
        #     queryset = queryset.filter(residential_assign_meter__user__first_name=name) | queryset.filter(residential_assign_meter__user__last_name=name)
        
        data = {
            'total_gas_used': total_gas_used,
            'total_quantity_purchased': total_quantity_purchased,
            #'total_transactional_amount': total_transactional_amount,
            'meter_readings': queryset.order_by('-last_push').first()
        }

        return data




'''
1. unassigned cylinder a
2. onboard/assign cylinder & meter a
3. get reading from that assigned meter and get the 
'''



# Cylinder Detail View
@api_view(['GET'])
@permission_classes((AllowAny,))
def GasReadingHistoryssAPIView(self, smart_box_id):
    """ API for Meter Reading History by Meter_id """
    try:
        smart_meter = SmartBox.objects.get(box_id=smart_box_id) 
        print(f'checking meter_id.. => {smart_meter}')
        gas_reading_serializer = CollectGasReadingsSerializer(smart_meter)
        return Response({"message": "success", "data": gas_reading_serializer.data}, status=status.HTTP_200_OK)
    except SmartBox.DoesNotExist:
        return Response({"message": "SmartBox not found!"}, status=status.HTTP_400_BAD_REQUEST)



class GasReadingHistoryAPIView(generics.ListAPIView):
    serializer_class = ResidentialCustomersGasReadingsSerializer

    def get_queryset(self):
        meter_id = self.kwargs['smart_box_id']
        print(f'checking meter_id.. => {meter_id}')

        
        try:
            smart_meter = self.kwargs['smart_box_id']
            #smart_meter = SmartBox.objects.get(box_id=meter_id) 
            print(f'checking meter_id.. => {smart_meter}')
            return CollectGasReading.objects.filter(smart_box_id=smart_meter)
        except SmartBox.DoesNotExist:
            return CollectGasReading.objects.none()

    def list(self, request, *args, **kwargs):
        meter_id = self.kwargs['smart_box_id']
        
        try:
            smart_meter = SmartBox.objects.get(box_id=meter_id)
            queryset = self.filter_queryset(self.get_queryset())
            
            if not queryset.exists():
                return Response({'detail': 'No gas reading history found.'}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except SmartBox.DoesNotExist:
            return Response({'detail': 'Invalid meter ID.'}, status=status.HTTP_400_BAD_REQUEST)



class UserGasConsumptionAndCostAPIView(APIView):
    """ API to Get User Gas Consumption & Cost Details """
    def get(self, request, user_id):
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        # Check if GasMeterStatus records exist for the user
        gas_meter_status_exists = GasMeterStatus.objects.filter(user_id=user_id).exists()

        total_gas_quantity_purchased = 0
        total_transactional_amount = 0
        total_quantity_used = 0
        total_gas_amount = 0
        total_gas_cost = 0
        total_gas_consumption = 0
        remaining_gas_quantity = 0
        virtual_wallet_balance = 'null'
        virtual_wallet_debt = 'null'
        smart_box_id = 'null'


        if gas_meter_status_exists:
            total_gas_consumption = GasMeterStatus.objects.filter(user_id=user_id).aggregate(total_gas_consumption=
            Sum('quantity_used'))['total_gas_consumption']
            #gas_cost = GasMeterStatus.objects.filter(user_id=user_id).aggregate(total_gas_cost=Sum('quantity_used'))['total_gas_cost']
            # Replace 'OtherBillModel' with the actual model representing other billable costs
            #other_billable_costs = OtherBillModel.objects.filter(user_id=user_id).aggregate(total_cost=Sum('amount'))['total_cost']
            smart_box_id = GasMeterStatus.objects.filter(user_id=user.id).values_list('smart_box', flat=True).first()

       
            # Calculate the remaining gas quantity (quantity_gas_left) for the user
            remaining_gas_quantity = GasMeterStatus.objects.filter(user_id=user_id).latest('last_push').quantity_gas_left
        

            # Calculate the total gas quantity purchased by the user
            total_gas_quantity_purchased = GasMeterStatus.objects.filter(user_id=user_id).aggregate(total_gas_quantity_purchased=
                Sum('quantity_supplied'))['total_gas_quantity_purchased']
            total_quantity_used = GasMeterStatus.objects.filter(user_id=user.id).aggregate(total_quantity_used=
                Sum('quantity_used'))['total_quantity_used']

            # Calculate the total cost of gas for the user (assuming a fixed cost per unit of gas)
            unit_cost_of_gas = 250 #untrue value
            other_billable_costs = 1000 # untrue value
            #total_gas_amount = total_quantity_used * <amount_per_unit_of_gas>
            total_gas_cost = total_gas_quantity_purchased * unit_cost_of_gas

            total_transactional_amount = total_gas_cost + other_billable_costs
            total_cost = total_gas_cost
            
            # Get the user's virtual wallet details
            #wallet = Wallet.objects.get(user=user)

            # Get or create the Wallet object for the user
            wallet, created = Wallet.objects.get_or_create(user=user)
            virtual_wallet_balance = wallet.balance
            virtual_wallet_debt = wallet.debt


        data = {
            'full_name': user.get_full_name(),
            'smart_box_id': smart_box_id,
            'quantity_remaining':remaining_gas_quantity,
            #'total_gas_consumption': total_gas_consumption,
            'total_gas_amount': total_gas_cost,
            'total_gas_quantity_purchased':total_gas_quantity_purchased,
            'total_transactional_amount': total_transactional_amount,
            #'total_quantity_used':total_quantity_used,
            'virtual_wallet_balance': virtual_wallet_balance,
            'debt': virtual_wallet_debt
        }
        
        return Response(data)


class CreateActivatedSmartboxReadingView(generics.CreateAPIView):
    """ API to Create SmartBox Readings From SmartBox Hardware/Device """
    queryset = ActivatedSmartBoxReading.objects.all()
    serializer_class = ActivatedSmartboxReadingSerializer

    def post(self, request, *args, **kwargs):
        serializer = SmartBoxReadingsSerializer(data=request.data)
        if serializer.is_valid():
            which_smartbox = request.data.get('smart_box_id')
            qty_used = request.data.get('quantity_used')
            battery_remaining = request.data.get('battery_remaining')
            longitude = request.data.get('longitude')
            latitude = request.data.get('latitude')

            # Perform calculations
            
            if ResidentialAssignCylinder.objects.filter(smart_box=which_smartbox).exists():
                print('Loading ...! SmartBox Exists!! ... Gas Reading Activated!!!')

                cylinder_attached_to_smartbox = ActivatedReading.objects.create(
                    smart_box_id = None
                )
            pass



class SmartBoxDefaultReadingsView(generics.ListAPIView):
    """ API For Unassigned/Default SmartBox Readings """
    queryset = SmartBoxReadings.objects.all()
    serializer_class = SmartBoxReadingsSerializer


# Activated Smartbox Readings
class ActivatedSmartBoxReadingsListView(generics.ListAPIView):
    """ API For Activated SmartBox Readings """
    queryset = ActivatedSmartBoxReading.objects.all()
    serializer_class = ActivatedSmartboxReadingSerializer


class AssignedSmartBoxReadingsView(generics.ListAPIView):
    """ API For Onboarded & Assigned SmartBox Readings """ 
    queryset = ResidentialAssignCylinder.objects.all()
    serializer_class = AssignedSmartBoxReadingsSerializer


class DetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SmartBoxReadings.objects.all()
    serializer_class = SmartBoxReadingsSerializer


class ReadLastByMeterView(generics.GenericAPIView):
    queryset = SmartBoxReadings.objects.all()
    serializer_class = SmartBoxReadingsSerializer

    def get_object(self):
        result = self.queryset.filter(meter=self.kwargs.get("meter"))
        return result

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, many=True)
        result = serializer.data[0]
        return Response(result)


class ReadLastTenValueByMeterView(generics.GenericAPIView):
    queryset = SmartBoxReadings.objects.all()
    serializer_class = SmartBoxReadingsSerializer

    def get_object(self):
        result = self.queryset.filter(meter=self.kwargs.get("meter"))
        return result

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, many=True)
        result = serializer.data[:10]
        return Response(result)


@api_view(["GET"])
def update_reading(self, request):
    # queryset = Reading.objects.filter(meter=self.kwargs.get('meter'))
    queryset = self.queryset.filter(meter=self.kwargs.get("meter"))
    # queryset = Reading.objects.all()
    # serializer = ReadingSerializer(request.POST, instance=queryset)
    print(queryset)

    # if serializer.is_valid():
    #     instance = serializer.save(commit=False)
    #     instance.total_quantity_used += instance.quantity_used
    #     instance.quantity_remaining = 12 - instance.total_quantity_used
    #     instance.save()
    return Response("worked")


class NewReadingUpdateView(generics.GenericAPIView):
    queryset = SmartBoxReadings.objects.all()
    serializer_class = SmartBoxReadingsSerializer

    def get_object(self):
        result = self.queryset.filter(meter=self.kwargs.get("meter"))
        return result

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, many=True)
        result = serializer.data[0]
        print(result, " result")

        i = 0
        total_sum = 0
        while i in range(len(serializer.data[:200])):
            used_quantity = float(serializer.data[i]["quantity_used"])
            used_quantity = used_quantity / 0.4
            print(used_quantity)
            total_sum += used_quantity
            i += 1

            if total_sum >= 12:
                total_sum = total_sum - 12
                i += -i
                print(i)
                break

        quant_rem = 12 - total_sum

        user = 1
        meter = "MIR001"
        cylinder_size = "12"
        date = datetime.date.today()
        access_code = uuid.uuid4().hex[:6].upper()
        status = "Pending"

        if 10.70 <= total_sum <= 10.75 or 10.80 <= total_sum <= 10.85:
            payload = {
                "user": user,
                "meter": meter,
                "cylinder_size": cylinder_size,
                "date": date,
                "access_code": access_code,
                "status": status,
            }

            r = requests.post("http://127.0.0.1:8001/api/v1/anorder/", data=payload)
            print(r.text)

            one_signal_url = "https://onesignal.com/api/v1/notifications"

            order_payload = {
                "app_id": "ca2c6082-8fa1-4836-82cb-593ece5f66ad",
                "include_external_user_ids": ["1"],
                "channel_for_external_user_ids": "push",
                "priority": 10,
                "headings": {"en": "Gas Swap Schedule"},
                "contents": {
                    "en": "You have been scheduled for delivery and swap due to low gas quantity. Access code {"
                    "delivery_access_code} for delivery personnel confirmation."
                },
            }
            order_headers = {
                "Authorization": "Basic MzU1YjQ1ZDgtYjc1MS00NjllLWJhZGYtZjMzNWM4MmFmZjk4"
            }

            output = requests.post(
                one_signal_url, headers=order_headers, json=order_payload
            )
            print(output.text)

        return Response(
            {
                "meter": result["meter"],
                "quantity_used": str(total_sum),
                "quantity_remaining": str(quant_rem),
                "battery_remaining": result["battery_remaining"],
                "last_push": datetime.datetime.now(),
            }
        )  # this is a makeshift time o


class RangeListCreateView(generics.ListCreateAPIView):
    queryset = Range.objects.all()
    serializer_class = RangeSerializer

    def post(self, request, *args, **kwargs):

        user = request.data.get("user")
        user_assignment = AssignMeterCylinder.objects.get(user_id=user)
        meter = str(user_assignment.meter)

        final_sum = 0
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response("Range cannot be fetched. Something happened")

        start_date = request.data.get("start_date")
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

        end_date = request.data.get("end_date")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        days = end_date - start_date
        number_of_days = days.days

        for i in range(number_of_days + 1):
            print("day ", i, ": ", start_date + datetime.timedelta(i))
            day_date = str(start_date + datetime.timedelta(i))
            read_url = "https://fornewhft.herokuapp.com/api/dailymeterreadingstotal/"
            value = requests.get(read_url + day_date + "/" + meter).json()
            print(value)
            final_sum += value["total_sum"]

        serializer.save()

        return Response(
            {
                "final_sum": final_sum,
                "days_between": str(number_of_days + 1),
                "message": "number of days includes start date",
            }
        )


class RangeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Range.objects.all()
    serializer_class = RangeSerializer


# if there is no reading yet, create one and save
class NewerReadingUpdateView(generics.GenericAPIView):
    queryset = SmartBoxReadings.objects.all()
    serializer_class = SmartBoxReadingsSerializer

    def get_object(self):
        result = self.queryset.filter(meter=self.kwargs.get("meter"))
        return result

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, many=True)
        result = serializer.data[0]
        previous_result = serializer.data[1]

        whole_sum = 0

        return Response("New reading works for now")

