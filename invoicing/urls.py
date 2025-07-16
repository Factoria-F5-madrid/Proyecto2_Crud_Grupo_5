from django.urls import path
from .views import (
    InvoiceListCreate,             # Vista para listar y crear facturas (aunque la creación se hará con la acción de abajo)
    InvoiceRetrieveUpdateDestroy,  # Vista para ver/editar/borrar una factura
    generate_client_invoice_view,      # La vista que contiene la lógica de negocio
    InvoiceStatusUpdate,           # Vista para cambiar el estado (ej. a pagada)
    GenerateInvoicePDF             # Vista para generar el PDF
)

urlpatterns = [
    # --- RUTAS PRINCIPALES PARA FACTURAS ---
    path('', InvoiceListCreate.as_view(), name='invoice-list'),
    path('<int:pk>/', InvoiceRetrieveUpdateDestroy.as_view(), name='invoice-detail'),

    # --- RUTAS PARA ACCIONES ESPECÍFICAS ---
    
    # 1. Endpoint para generar una nueva factura para un cliente
    path('generate-for-client/<int:client_id>/', generate_client_invoice_view, name='invoice-generate'),

    # 2. Endpoint para actualizar el estado de una factura (ej. marcar como pagada)
    path('<int:pk>/status/', InvoiceStatusUpdate.as_view(), name='invoice-status-update'),

    # 3. Endpoint para descargar el PDF
    path('<int:pk>/pdf/', GenerateInvoicePDF.as_view(), name='invoice-pdf'),
    
]