# clients/views.py
from rest_framework import generics
from .models import Client
from .serializers import ClientSerializer

class ClientListCreate(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filterset_fields = ['name', 'city', 'is_active']
    search_fields = ['name', 'tax_id', 'email']

class ClientRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer