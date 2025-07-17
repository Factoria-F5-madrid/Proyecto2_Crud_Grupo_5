from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Service, ServiceCategory
from .serializers import ServiceSerializer, ServiceCategorySerializer 
class ServiceCategoryListCreate(generics.ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    ordering = ['name']

class ServiceCategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer

class ServiceListCreate(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    filterset_fields = ['name', 'category', 'is_active']
    search_fields = ['name', 'code', 'description']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ServiceListSerializer
        return ServiceSerializer

class ServiceRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer