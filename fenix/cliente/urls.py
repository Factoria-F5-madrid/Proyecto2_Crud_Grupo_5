from django.urls import path
from .api_views import CustomerListCreateAPIView, CustomerRetrieveUpdateDestroyAPIView, export_customers_csv_api


app_name = 'cliente_api' # Un namespace específico para las URLs de API de 'cliente'

urlpatterns = [
    # URLs para la API REST de clientes
    path('customers/', CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerRetrieveUpdateDestroyAPIView.as_view(), name='customer-detail'),
    # NUEVA URL para exportar clientes a CSV via API
    path('customers/export-csv/', export_customers_csv_api, name='customer-export-csv'),
]