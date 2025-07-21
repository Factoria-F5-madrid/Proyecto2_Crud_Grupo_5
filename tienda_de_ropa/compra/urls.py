from django.urls import path
from . import views

app_name = 'compra' # Usa 'compra' para el namespacing

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('add/', views.order_create, name='order_create'),
    path('<int:pk>/edit/', views.order_update, name='order_update'),
    path('<int:pk>/delete/', views.order_delete, name='order_delete'),
    # Puedes añadir URLs para OrderItem si decides gestionarlos directamente
    # path('items/', views.order_item_list, name='order_item_list'),
    # path('items/<int:pk>/', views.order_item_detail, name='order_item_detail'),
    # ...
]