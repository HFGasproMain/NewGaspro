import datetime
import uuid
import requests
from rest_framework import generics, status
from rest_framework.decorators import api_view
from asset.models import RetailAssignCylinder
from .models import SmartBoxReadings, Range, ActivatedSmartBoxReading, CollectGasReading
from .serializers import SmartBoxReadingsSerializer, RangeSerializer, AssignedSmartBoxReadingsSerializer, \
 ActivatedSmartboxReadingSerializer, CollectGasReadingsSerializer
from rest_framework.response import Response



# All Views Here
class CollectGasReadingView(generics.CreateAPIView):
    """ API to Get Live SmartBox Readings From SmartBox Hardware/Device """
    queryset = CollectGasReading.objects.all()
    serializer_class = CollectGasReadingsSerializer

    def post(self, request, *args, **kwargs):
        serializer = SmartBoxReadingsSerializer(data=request.data)
        if serializer.is_valid():
            which_smart_box = request.data.get('smart_box_id')
            print(f'smart_box_id_received => {which_smart_box}')
            qty_used = request.data.get('quantity_used')
            battery_remaining = request.data.get('battery_remaining')
            longitude = request.data.get('longitude')
            latitude = request.data.get('latitude')

            # Perform all calculations
            assigned_meter = RetailAssignCylinder.objects.filter(smart_box=which_smart_box)

            if RetailAssignCylinder.objects.filter(smart_box=which_smart_box).exists():
                print('Loading ...! SmartBox Exists!! ... Gas Reading Activated!!!')
                get_smartbox = RetailAssignCylinder.objects.filter(smart_box=which_smart_box).first()
                print(f'smart_box_id_comparing... => {get_smartbox}')
                get_cylinder = RetailAssignCylinder.objects.filter(smart_box=which_smart_box).first()
                print(f'cylinder_comparing... => {get_cylinder}')
                get_user = RetailAssignCylinder.objects.filter()
                cylinder_attached_to_smartbox = ActivatedReading.objects.create(
                    smart_box_id = None
                )
                return Response({"message": "success", "data": serializer.data}, status=status.HTTP_200_OK)
                #RetailAssignCylinder.DoesNotExist:
            return Response({"message": "Cylinder not found!"}, status=status.HTTP_400_BAD_REQUEST)

'''
1. unassigned cylinder a
2. onboard/assign cylinder & meter a
3. get reading from that assigned meter and get the 
'''


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
            
            if RetailAssignCylinder.objects.filter(smart_box=which_smartbox).exists():
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
    queryset = RetailAssignCylinder.objects.all()
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

