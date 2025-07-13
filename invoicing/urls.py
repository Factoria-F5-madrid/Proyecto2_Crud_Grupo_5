from django.urls import path
from .views import (
    InvoiceListCreate, 
    InvoiceRetrieveUpdateDestroy,
    InvoiceItemCreate,
    InvoiceItemRetrieveUpdateDestroy,
    InvoiceStatusUpdate,
    GenerateInvoicePDF
)

urlpatterns = [
    path('', InvoiceListCreate.as_view(), name='invoice-list-create'),
    path('<int:pk>/', InvoiceRetrieveUpdateDestroy.as_view(), name='invoice-detail'),
    path('<int:invoice_id>/items/', InvoiceItemCreate.as_view(), name='invoice-item-create'),
    path('<int:invoice_id>/items/<int:pk>/', InvoiceItemRetrieveUpdateDestroy.as_view(), name='invoice-item-detail'),
    path('<int:pk>/status/', InvoiceStatusUpdate.as_view(), name='invoice-status-update'),
    path('<int:pk>/pdf/', GenerateInvoicePDF.as_view(), name='generate-invoice-pdf'),
]