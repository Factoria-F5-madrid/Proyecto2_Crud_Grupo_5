from django.urls import path
from . import views

app_name = 'categoria' # Usa 'categoria' para el namespacing

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('<int:pk>/', views.category_detail, name='category_detail'),
    path('add/', views.category_create, name='category_create'),
    path('<int:pk>/edit/', views.category_update, name='category_update'),
    path('<int:pk>/delete/', views.category_delete, name='category_delete'),
]