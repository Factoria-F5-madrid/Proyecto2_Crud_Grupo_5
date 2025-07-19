from django.urls import path, include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('api/', include('prendas.urls')),
    path('api/', include('clientes.urls')),
    path('api/', include('categorias.urls')),
    path('api/', include('ventas.urls')),
    path('api/', include('usuarias.urls')),
]
