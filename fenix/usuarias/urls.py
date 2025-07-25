from django.urls import path
from .api_views import (
    UsuariaListCreateAPIView,
    UsuariaRetrieveUpdateDestroyAPIView,
    export_usuarias_csv_api,
    reactivate_usuaria_api,
    usuarias_statistics_api
)

app_name = 'usuarias_api'

urlpatterns = [
    # CRUD endpoints for usuarias
    path('usuarias/', UsuariaListCreateAPIView.as_view(), name='usuaria-list-create'),
    path('usuarias/<int:pk>/', UsuariaRetrieveUpdateDestroyAPIView.as_view(), name='usuaria-detail'),
    
    # Additional endpoints
    path('usuarias/export-csv/', export_usuarias_csv_api, name='usuaria-export-csv'),
    path('usuarias/<int:pk>/reactivate/', reactivate_usuaria_api, name='usuaria-reactivate'),
    path('usuarias/statistics/', usuarias_statistics_api, name='usuaria-statistics'),
]
