from django.urls import path
from .views_api import CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView

app_name = 'categoría_api'

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
]
