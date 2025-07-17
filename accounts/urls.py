from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, ChangePasswordView # Asume que tienes estas vistas

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    # Si tienes un UserViewSet, también lo incluirías aquí
    # path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    # path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),
]