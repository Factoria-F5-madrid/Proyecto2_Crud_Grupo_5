from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
import csv
from .models import Usuaria
from .serializers import UsuariaSerializer, UsuariaListSerializer, UsuariaCreateSerializer
from django_filters import rest_framework as django_filters

class UsuariaFilter(django_filters.FilterSet):
    """Custom filter for usuarias"""
    hire_date_from = django_filters.DateFilter(field_name="hire_date", lookup_expr='gte')
    hire_date_to = django_filters.DateFilter(field_name="hire_date", lookup_expr='lte')
    salary_min = django_filters.NumberFilter(field_name="salary", lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name="salary", lookup_expr='lte')
    
    class Meta:
        model = Usuaria
        fields = {
            'role': ['exact'],
            'status': ['exact'],
            'is_active': ['exact'],
        }

class UsuariaListCreateAPIView(generics.ListCreateAPIView):
    """
    Vista para listar todas las usuarias activas o crear una nueva.
    - GET /api/usuarias/ (Lista todas las usuarias activas con filtros)
    - POST /api/usuarias/ (Crea una nueva usuaria con avatar)
    
    Por defecto solo muestra usuarias activas (is_active=True).
    Para ver todas incluyendo inactivas, usar: ?show_all=true
    
    Filtros disponibles:
    - ?search=nombre (busca en nombre, apellido, username, email)
    - ?role=ADMIN (filtra por rol: ADMIN, EMPLOYEE, MANAGER)
    - ?status=ACTIVE (filtra por estado: ACTIVE, INACTIVE, SUSPENDED)
    - ?is_active=true (filtra por activas/inactivas)
    - ?show_all=true (incluye usuarias inactivas)
    - ?hire_date_from=2023-01-01&hire_date_to=2023-12-31 (rango de fechas contratación)
    - ?salary_min=1000&salary_max=5000 (rango salarial)
    - ?ordering=first_name,-created_at (ordena por campos)
    
    Para subir avatar: usar Content-Type: multipart/form-data
    """
    queryset = Usuaria.objects.filter(is_active=True)
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = UsuariaFilter
    search_fields = ['first_name', 'last_name', 'username', 'email']
    ordering_fields = ['first_name', 'last_name', 'username', 'created_at', 'hire_date']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Override queryset to handle show_all parameter"""
        queryset = Usuaria.objects.all()
        
        # Por defecto, solo mostrar usuarias activas
        show_all = self.request.query_params.get('show_all', 'false').lower()
        if show_all != 'true':
            queryset = queryset.filter(is_active=True)
            
        return queryset
    
    def get_serializer_class(self):
        """Use different serializers for list vs create"""
        if self.request.method == 'GET':
            return UsuariaListSerializer
        return UsuariaCreateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            # Return full usuaria data after creation
            usuaria = serializer.instance
            response_serializer = UsuariaSerializer(usuaria, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuariaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para recuperar, actualizar o eliminar una usuaria específica.
    - GET /api/usuarias/{id}/ (Obtiene los detalles de una usuaria)
    - PUT /api/usuarias/{id}/ (Actualiza una usuaria existente con avatar)
    - PATCH /api/usuarias/{id}/ (Actualiza parcialmente una usuaria existente)
    - DELETE /api/usuarias/{id}/ (Elimina una usuaria)
    
    Para actualizar avatar: usar Content-Type: multipart/form-data
    """
    queryset = Usuaria.objects.all()
    serializer_class = UsuariaSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    lookup_field = 'pk'
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete - mark as inactive instead of deleting"""
        instance = self.get_object()
        instance.is_active = False
        instance.status = 'INACTIVE'
        instance.save()
        return Response(
            {'detail': 'Usuaria marcada como inactiva exitosamente.'}, 
            status=status.HTTP_200_OK
        )

@api_view(['GET'])
def export_usuarias_csv_api(request):
    """
    Vista de API para exportar todas las usuarias a un archivo CSV.
    Accesible via GET a /api/usuarias/export-csv/
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="usuarias.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Username', 'Nombre', 'Apellido', 'Email', 'Teléfono',
        'Rol', 'Estado', 'Fecha Contratación', 'Salario', 'Activa', 'Fecha Creación'
    ])

    usuarias = Usuaria.objects.all().order_by('id')
    for usuaria in usuarias:
        writer.writerow([
            usuaria.id,
            usuaria.username,
            usuaria.first_name,
            usuaria.last_name,
            usuaria.email,
            usuaria.phone or '',
            usuaria.get_role_display(),
            usuaria.get_status_display(),
            usuaria.hire_date.strftime('%Y-%m-%d') if usuaria.hire_date else '',
            usuaria.salary or '',
            'Sí' if usuaria.is_active else 'No',
            usuaria.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response

@api_view(['POST'])
def reactivate_usuaria_api(request, pk):
    """
    Vista de API para reactivar una usuaria inactiva.
    Accesible via POST a /api/usuarias/{id}/reactivate/
    """
    try:
        usuaria = Usuaria.objects.get(pk=pk)
        usuaria.is_active = True
        usuaria.status = 'ACTIVE'
        usuaria.save()
        
        serializer = UsuariaSerializer(usuaria, context={'request': request})
        return Response({
            'detail': 'Usuaria reactivada exitosamente.',
            'usuaria': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Usuaria.DoesNotExist:
        return Response(
            {'detail': 'Usuaria no encontrada.'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
def usuarias_statistics_api(request):
    """
    Vista de API para obtener estadísticas de usuarias.
    Accesible via GET a /api/usuarias/statistics/
    """
    from django.db.models import Count, Avg
    
    stats = {
        'total_usuarias': Usuaria.objects.count(),
        'usuarias_activas': Usuaria.objects.filter(is_active=True).count(),
        'usuarias_inactivas': Usuaria.objects.filter(is_active=False).count(),
        'por_rol': list(
            Usuaria.objects.values('role')
            .annotate(count=Count('role'))
            .order_by('role')
        ),
        'por_estado': list(
            Usuaria.objects.values('status')
            .annotate(count=Count('status'))
            .order_by('status')
        ),
        'salario_promedio': Usuaria.objects.filter(
            salary__isnull=False
        ).aggregate(avg_salary=Avg('salary'))['avg_salary']
    }
    
    return Response(stats, status=status.HTTP_200_OK)
