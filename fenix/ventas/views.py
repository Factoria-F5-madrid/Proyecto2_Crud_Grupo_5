import django_filters
from rest_framework import viewsets
from .models import Venta
from .serializers import VentaSerializer
from django_filters.rest_framework import DjangoFilterBackend

class VentaFilter(django_filters.FilterSet):
    usuaria = django_filters.NumberFilter(field_name="usuaria") # filtra por ID de usuaria
    fecha_inicio = django_filters.DateTimeFilter(field_name="fecha", lookup_expr='gte')
    fecha_fin = django_filters.DateTimeFilter(field_name="fecha", lookup_expr='lte')
    
    class Meta:
        model = Venta
        fields = ['cliente', 'prenda', 'usuaria', 'fecha_inicio', 'fecha_fin']

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VentaFilter
    
    def perform_create(self, serializer):
        serializer.save(usuaria=self.request.user)

