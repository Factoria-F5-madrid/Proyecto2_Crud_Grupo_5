# compra/urls_api.py (Este archivo NO CAMBIA respecto a la versión anterior)
from django.urls import path
from .api_views import (
    OrderListCreateAPIView,
    OrderRetrieveUpdateDestroyAPIView,
    OrderItemListCreateAPIView,
    OrderItemRetrieveUpdateDestroyAPIView,
    export_orders_csv_api, export_order_items_csv_api # NUEVAS IMPORTACIONES
)

app_name = 'compra_api'

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyAPIView.as_view(), name='order-detail'),

    # Estas URLs para OrderItem individual son opcionales si solo quieres gestionarlos a través de Order
    path('order-items/', OrderItemListCreateAPIView.as_view(), name='orderitem-list-create'),
    path('order-items/<int:pk>/', OrderItemRetrieveUpdateDestroyAPIView.as_view(), name='orderitem-detail'),
    # NUEVAS URLs para exportar
    path('orders/export-csv/', export_orders_csv_api, name='order-export-csv'),
    path('order-items/export-csv/', export_order_items_csv_api, name='orderitem-export-csv'),
]