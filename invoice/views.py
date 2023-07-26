from django.shortcuts import render
from rest_framework import generics, pagination
from .models import Invoice
from .serializers import InvoiceSerializer

# Create your views here.
class InvoiceListView(generics.ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    pagination_class = pagination.LimitOffsetPagination
