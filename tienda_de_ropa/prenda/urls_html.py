from django.urls import path
from . import views # Importa las vistas de tu app 'prenda' (asumo que estas son tus vistas HTML)

app_name = 'prenda' # Esto es útil para el "namespacing" en las plantillas

urlpatterns = [
    
    # --- URLs para las VISTAS HTML (Interfaz de usuario web) ---
    # Estas URLs serán accesibles bajo el prefijo que le dé el urls.py principal (ej: /prenda/)
    # URL para la lista de productos
    path('', views.product_list, name='product_list'), # /prenda/
    # URL para el detalle de un producto específico (usando su ID, 'pk' es Primary Key)
    path('<int:pk>/', views.product_detail, name='product_detail'), # /prenda/1/
    # URL para añadir un nuevo producto
    path('add/', views.product_create, name='product_create'), # /prenda/add/
    # URL para editar un producto existente
    path('<int:pk>/edit/', views.product_update, name='product_update'), # /prenda/1/edit/
    # URL para eliminar un producto existente
    path('<int:pk>/delete/', views.product_delete, name='product_delete'), # /prenda/1/delete/
]
