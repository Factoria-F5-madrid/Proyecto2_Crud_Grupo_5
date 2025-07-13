from django.urls import path
from .views import ClientListCreate, ClientRetrieveUpdateDestroy

urlpatterns = [
    path('', ClientListCreate.as_view(), name='client-list-create'),
    path('<int:pk>/', ClientRetrieveUpdateDestroy.as_view(), name='client-detail'),
]