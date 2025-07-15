from django.urls import path, include

urlpatterns = [
    # Incluye las URLs de dj-rest-auth para login, logout, etc.
    path('', include('dj_rest_auth.urls')),
    # Incluye las URLs de registro si también usas dj-rest-auth para ello
    path('registration/', include('dj_rest_auth.registration.urls')),
]