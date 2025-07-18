from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Prenda
from .serializers import PrendaSerializer

class PrendaListCreateView(ListCreateAPIView):
    queryset = Prenda.objects.all()
    serializer_class = PrendaSerializer
# Create your views here.
