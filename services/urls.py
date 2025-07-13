from django.urls import path
from .views import ServiceListCreate, ServiceRetrieveUpdateDestroy, ServiceCategoryListCreate, ServiceCategoryRetrieveUpdateDestroy

urlpatterns = [
    path('', ServiceListCreate.as_view(), name='service-list-create'),
    path('<int:pk>/', ServiceRetrieveUpdateDestroy.as_view(), name='service-detail'),
    path('categories/', ServiceCategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', ServiceCategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),
]