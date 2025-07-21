# tienda_de_ropa/cliente/urls.py
from django.urls import path
from . import views # Correcto, importa las vistas de esta app

# app_name = 'cliente' # Mantén esta línea para el namespacing
app_name = 'cliente'

urlpatterns = [
    # Estas son las URLs específicas de la aplicación 'cliente'
    path('', views.customer_list, name='customer_list'),
    path('<int:pk>/', views.customer_detail, name='customer_detail'),
    path('add/', views.customer_create, name='customer_create'),
    path('<int:pk>/edit/', views.customer_update, name='customer_update'),
    path('<int:pk>/delete/', views.customer_delete, name='customer_delete'),
]