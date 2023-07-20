from rest_framework import generics
from .models import Card
from .serializers import CardSerializer


# All views here

class CardCreateView(generics.CreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

# class CardListView(generics.ListAPIView):
#     queryset = Card.objects.all()
#     serializer_class = CardSerializer


class UserCardDetailView(generics.RetrieveAPIView):
    serializer_class = CardSerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        queryset = Card.objects.all()
        user_id = self.request.query_params.get('user_id')
        #user_first_name = self.request.query_params.get('user_first_name')
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

class CardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class CardListView(generics.ListAPIView):
    serializer_class = CardSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Card.objects.filter(user_id=user_id)
