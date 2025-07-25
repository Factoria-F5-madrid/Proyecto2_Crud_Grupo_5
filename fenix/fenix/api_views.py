from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    """
    API Root - Lista todos los endpoints disponibles con enlaces navegables
    """
    return Response({
        'message': 'Bienvenido a la API de Fenix - Sistema de Gestión de Tienda de Ropa',
        'version': '2.0.0',
        'documentation': 'Haz clic en los enlaces para probar los endpoints directamente',
        'endpoints': {
            'categories': {
                'list_create': reverse('categoría_api:category-list-create', request=request, format=format),
                'detail': 'http://example.com/api/categories/{id}/',
                'description': 'CRUD para categorías de productos'
            },
            'products': {
                'list_create': reverse('prenda_api:product-list-create', request=request, format=format),
                'detail': 'http://example.com/api/products/{id}/',
                'export_csv': reverse('prenda_api:product-export-csv', request=request, format=format),
                'description': 'CRUD para productos con soporte de imágenes y filtros avanzados'
            },
            'customers': {
                'list_create': reverse('cliente_api:customer-list-create', request=request, format=format),
                'detail': 'http://example.com/api/customers/{id}/',
                'export_csv': reverse('cliente_api:customer-export-csv', request=request, format=format),
                'description': 'CRUD para clientes'
            },
            'orders': {
                'list_create': reverse('compra_api:order-list-create', request=request, format=format),
                'detail': 'http://example.com/api/orders/{id}/',
                'order_items': reverse('compra_api:orderitem-list-create', request=request, format=format),
                'export_orders_csv': reverse('compra_api:order-export-csv', request=request, format=format),
                'export_items_csv': reverse('compra_api:orderitem-export-csv', request=request, format=format),
                'description': 'CRUD para pedidos con items anidados'
            },
            'usuarias': {
                'list_create': reverse('usuarias_api:usuaria-list-create', request=request, format=format),
                'detail': 'http://example.com/api/usuarias/{id}/',
                'export_csv': reverse('usuarias_api:usuaria-export-csv', request=request, format=format),
                'statistics': reverse('usuarias_api:usuaria-statistics', request=request, format=format),
                'reactivate': 'http://example.com/api/usuarias/{id}/reactivate/',
                'description': 'CRUD para usuarias del sistema con avatars y estadísticas'
            }
        },
        'features': [
            'Filtros avanzados con django-filter',
            'Búsqueda en texto completo',
            'Ordenamiento múltiple',
            'Paginación automática',
            'Exportación CSV',
            'Subida de imágenes para productos y avatars',
            'CORS habilitado para frontend',
            'Validación robusta de datos',
            'Manejo de errores comprehensivo',
            'Estadísticas y reportes',
            'Soft delete para usuarias'
        ],
        'examples': {
            'filter_products': 'GET /api/products/?category=1&price_min=10&price_max=100',
            'search_customers': 'GET /api/customers/?search=juan',
            'order_by_date': 'GET /api/orders/?ordering=-order_date',
            'create_order': 'POST /api/orders/ with nested items',
            'upload_product_image': 'POST /api/products/ with multipart/form-data',
            'filter_usuarias': 'GET /api/usuarias/?role=ADMIN&is_active=true',
            'usuarias_stats': 'GET /api/usuarias/statistics/'
        }
    })
