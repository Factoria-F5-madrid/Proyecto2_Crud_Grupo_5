from django.urls import path
from .api_views import CustomerListCreateAPIView, CustomerRetrieveUpdateDestroyAPIView

app_name = 'cliente_api' # Un namespace específico para las URLs de API de 'cliente'

urlpatterns = [
    # URLs para la API REST de clientes
    path('customers/', CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerRetrieveUpdateDestroyAPIView.as_view(), name='customer-detail'),
]