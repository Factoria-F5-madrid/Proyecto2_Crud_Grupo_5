from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .api_views import api_root
from django.conf import settings

urlpatterns = [
    path('', api_root, name='api-root'),
    path('api/', api_root, name='api-root-api'),
    path('admin/', admin.site.urls),
    path('api/', include('prenda.urls')),
    path('api/', include('cliente.urls')),
    path('api/', include('categoría.urls')),
    path('api/', include('compra.urls')),
    path('api/', include('usuarias.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

