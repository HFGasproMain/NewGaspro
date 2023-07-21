from rest_framework import generics
from .models import Card
from .serializers import CardSerializer


# All views here

class CardCreateView(generics.CreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class CardListView(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class UserCardDetailView(generics.RetrieveAPIView):
    serializer_class = CardSerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        queryset = Card.objects.all()
        user_id = self.request.query_params.get('user_id')
        #user_first_name = self.request.query_params.get('user_first_name')

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        # if user_first_name:
        #     users = User.objects.filter(first_name__icontains=user_first_name)
        #     queryset = queryset.filter(user__in=users)
        return queryset

class CardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class UserCardListView(generics.ListAPIView):
    serializer_class = CardSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        p = Card.objects.filter(user_id=user_id)
        print(f'p is: {p}')
        return p