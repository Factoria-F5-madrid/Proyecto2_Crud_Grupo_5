# tienda_de_ropa/tienda_de_ropa/urls.py

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
    path('productos/', include('prenda.urls_html')),
    # Incluye las URLs de 'categoría'. Si este archivo 'categoría/urls.py' contiene vistas HTML,
    # entonces esta línea es correcta. Si no tienes vistas HTML para categoría,
    # o si este archivo es un remanente de una configuración anterior de API,
    # podrías considerar eliminarlo para evitar confusión o redundancia.
    path('categorias/', include('categoría.urls')),
    path('clientes/', include('cliente.urls')),
    path('compras/', include('compra.urls')),

    # --- URLs para las APIs REST ---
    # Incluye las URLs API de 'prenda' bajo el prefijo '/api/'
    # Usamos el namespace definido en prenda/urls_api.py
    path('api/', include('prenda.urls_api', namespace='api_prenda')),
    # ¡LÍNEA IMPORTANTE!
    # Aquí incluimos todas las URLs definidas en 'categoria/urls_api.py'.
    # 'api/categorias/' será el prefijo para todas esas URLs.
    # Por ejemplo, la ruta '' en urls_api.py se convertirá en '/api/categorias/'.
    # Y la ruta '<int:pk>/' se convertirá en '/api/categorias/<int:pk>/'.
    # El 'namespace' debe coincidir con el 'app_name' que definimos en categoria/urls_api.py
    path('api/categorias/', include('categoría.urls_api', namespace='categoria_api')),
    # Aquí es donde, en el futuro, incluirías las URLs de API para otras aplicaciones (cliente, compra)
    # Ejemplo futuro: path('api/clientes/', include('cliente.urls_api', namespace='cliente_api')),
]
