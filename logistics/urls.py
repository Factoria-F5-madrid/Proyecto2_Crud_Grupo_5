from django.urls import path
from .views import (
    ShipmentListCreate, 
    ShipmentRetrieveUpdateDestroy, 
    CategoryListCreate, 
    CategoryRetrieveUpdateDestroy
)

urlpatterns = [
    # URLs para el modelo Shipment
    path('', ShipmentListCreate.as_view(), name='shipment-list-create'),
    path('<int:pk>/', ShipmentRetrieveUpdateDestroy.as_view(), name='shipment-detail'),

    # URLs para el modelo Category
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),
]