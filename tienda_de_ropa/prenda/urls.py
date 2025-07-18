from django.urls import path
from . import views # Importa las vistas de tu app 'prenda'


app_name = 'prenda' # Esto es útil para el "namespacing" en las plantillas

urlpatterns = [
    # URL para la lista de productos
    path('', views.product_list, name='product_list'),
    # URL para el detalle de un producto específico (usando su ID, 'pk' es Primary Key)
    path('<int:pk>/', views.product_detail, name='product_detail'),
    # URL para añadir un nuevo producto
    path('add/', views.product_create, name='product_create'),
    # URL para editar un producto existente
    path('<int:pk>/edit/', views.product_update, name='product_update'),
    # URL para eliminar un producto existente
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
   
]