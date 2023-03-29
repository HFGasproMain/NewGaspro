from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.models import User
#from retailer.models import Retailer
from .models import Auxiliary #RetailerAuxiliary
from .serializers import AuxiliarySerializer #RetailerAuxiliarySerializer
from rest_framework import generics, status


class AuxiliaryDetailByUserView(generics.UpdateAPIView):
    queryset = Auxiliary.objects.all()
    serializer_class = AuxiliarySerializer

    def get_object(self):
        result = generics.get_object_or_404(self.queryset, customer=self.kwargs.get("customer"))
        return result

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AuxiliaryCreateView(generics.CreateAPIView):
    queryset = Auxiliary.objects.all()
    serializer_class = AuxiliarySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Error adding auxiliary, Try again!"},status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        user_id = int(request.data.get("customer"))

        '''
        one_signal_url = "https://onesignal.com/api/v1/notifications"
        on_board_payload = {
            "app_id": app_id,
            "include_external_user_ids": [str(user_id)],
            "channel_for_exterrnal_user_ids": "push",
            "priority": 10,
            "headings": {"en": "Hommie from Homefort"},
            "contents": {
                "en": 'Hi {{first_name | default: "there"}}, we at Homefort Energy are happy to receive '
                "you. Kindly add your card details to enjoy automated gas delivery while you focus "
                "on what matters. We love you :)"
            },
        }
        on_board_headers = {"Authorization": auth_header}

        requests.post(one_signal_url, headers=on_board_headers, json=on_board_payload)

        payload = {
            "user": user_id,
            "content": "Welcome to Homefort Energy",
            "notif_type": "Blue",
            "date": datetime.date.today(),
        }
        requests.post(
            "https://newhftapp2.herokuapp.com/api/v1/notifications/", data=payload
        )
        '''
        # meters = unassigned_meters_list()
        # cylinders = unassigned_cylinders_list()
        # assignable_meter = meters[0]["meter"]
        # assignable_cylinder = cylinders[0]["cylinder_serial_number"]
        #
        # data = {
        #     "user": int(user_id),
        #     "meter": assignable_meter,
        #     "cylinder": assignable_cylinder,
        #     "date_assigned": datetime.datetime.now(),
        # }
        #
        # url = "http://newhftapp2.herokuapp.com/api/v1/assignment/"
        # resp = requests.post(url, data=data)
        # print(resp)

        return Response(serializer.data)


class AuxiliaryListView(generics.ListAPIView):
    queryset = Auxiliary.objects.all()
    serializer_class = AuxiliarySerializer


class AuxiliaryUpdateView(generics.UpdateAPIView):
    queryset = Auxiliary.objects.all()
    serializer_class = AuxiliarySerializer


class AuxiliaryDeleteView(generics.DestroyAPIView):
    queryset = Auxiliary.objects.all()
    serializer_class = AuxiliarySerializer


class AuxiliaryDetailView(generics.RetrieveAPIView):
    queryset = Auxiliary.objects.all()
    serializer_class = AuxiliarySerializer



# class RetailerAuxiliaryCreateView(generics.CreateAPIView):
#     queryset = RetailerAuxiliary.objects.all()
#     serializer_class = RetailerAuxiliarySerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         if not serializer.is_valid(raise_exception=True):
#             return Response(
#                 {"message": "Something went wrong. Try later"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         retailer = request.data.get("retailer")
#         if not Retailer.objects.filter(id=retailer).exists():
#             return Response(
#                 {"message": "No retailer exists with this ID"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         retailer_object = Retailer.objects.get(id=retailer)
#         user_id = retailer_object.user.id
#         user_object = User.objects.get(id=user_id)

#         if serializer.is_valid():
#             serializer.save(customer=user_object)

#         return Response(
#             {"message": "Retailer auxiliary successfully added"},
#             status=status.HTTP_201_CREATED,
#         )


# class RetailerAuxiliaryListView(generics.ListAPIView):
#     queryset = RetailerAuxiliary.objects.all()
#     serializer_class = RetailerAuxiliarySerializer


# class RetailerAuxiliaryDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = RetailerAuxiliary.objects.all()
#     serializer_class = RetailerAuxiliarySerializer


# @api_view(["GET"])
# def retailer_auxiliary_by_retailer(self, retailer_id):
#     try:
#         # retailer_aux = RetailerAuxiliarySerializer(
#         #     RetailerAuxiliary.objects.get(retailer_id=retailer_id)
#         # )

#         retailer_aux = list(
#             RetailerAuxiliary.objects.filter(retailer_id=retailer_id).values()
#         )
#         # return Response(retailer_aux.data, status=status.HTTP_200_OK)
#         return Response(retailer_aux, status=status.HTTP_200_OK)
#     except Retailer.DoesNotExist:
#         return Response({}, status=status.HTTP_200_OK)
#     except User.DoesNotExist:
#         return Response({}, status=status.HTTP_200_OK)
#     except RetailerAuxiliary.DoesNotExist:
#         return Response({}, status=status.HTTP_200_OK)
