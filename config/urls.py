from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static# Importa tu vista protegida real
from accounts.views import ProtectedTestView # Asegúrate de que esta vista esté definida en accounts/views.py

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Añade la URL para tu vista protegida real aquí
    path('api/protected-resource/', ProtectedTestView.as_view(), name='protected_resource_test'),
    path('api/clients/', include('clients.urls')),
    path('api/services/', include('services.urls')),
    path('api/invoices/', include('invoicing.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    
    # React App - debe estar al final para capturar todas las demás URLs
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]

# Añadir configuración para archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    

