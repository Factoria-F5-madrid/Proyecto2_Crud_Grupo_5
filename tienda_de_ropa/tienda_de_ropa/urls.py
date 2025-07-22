"""
URL configuration for tienda_de_ropa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # --- URLs para las VISTAS HTML ---
    # Incluye las URLs HTML de 'prenda' bajo el prefijo '/productos/'
    path('productos/', include('prenda.urls_html')), # ¡Aquí cambiamos a urls_html!   
    path('categorias/', include('categoría.urls')),
    path('clientes/', include('cliente.urls_html')), # ¡Aquí se incluye el urls_html de cliente!
    path('compras/', include('compra.urls')),

    # --- URLs para las APIs REST ---
    # Incluye las URLs API de 'prenda' bajo el prefijo '/api/'
    # Usamos el namespace definido en prenda/urls_api.py
    path('api/', include('prenda.urls_api', namespace='api_prenda')), # ¡Aquí cambiamos a urls_api!
    path('api/', include('cliente.urls_api', namespace='api_cliente')), # Incluye las URLs API de cliente
]