from django.urls import path
from . import views # Importa todas las vistas de compra
from .views import OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView, order_detail
# Si OrderItemForm se va a usar en estas vistas, asegúrate de que exista y se importe correctamente.
# from .views import OrderItemCreateView, OrderItemUpdateView, OrderItemDeleteView


app_name = 'compra' # Define el espacio de nombres de la aplicación

urlpatterns = [
    # URLs para el modelo Order (Pedido)
    # Lista de pedidos
    path('', OrderListView.as_view(), name='order_list'), # CAMBIO AQUÍ: Añadir la coma
    path('crear/', OrderCreateView.as_view(), name='order_create'), # Vista para crear un nuevo pedido
    path('<int:pk>/', order_detail, name='order_detail'), # Detalle de un pedido (función-based view)
    path('<int:pk>/editar/', OrderUpdateView.as_view(), name='order_update'), # Vista para editar un pedido
    path('<int:pk>/eliminar/', OrderDeleteView.as_view(), name='order_delete'), # Vista para eliminar un pedido

    # # URLs para el modelo OrderItem (Ítem de Pedido) - Descomentar si usas estas vistas
    # path('items/crear/', OrderItemCreateView.as_view(), name='orderitem_create'),
    # path('items/<int:pk>/editar/', OrderItemUpdateView.as_view(), name='orderitem_update'),
    # path('items/<int:pk>/eliminar/', OrderItemDeleteView.as_view(), name='orderitem_delete'),
]