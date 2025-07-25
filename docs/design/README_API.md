# Fenix - API de Gestión de Tienda de Ropa

## 🚀 Características Principales

- **API REST Completa** con Django REST Framework
- **Filtros Avanzados** usando django-filter
- **Búsqueda de Texto Completo** en múltiples campos
- **Paginación Automática** (20 elementos por página)
- **Exportación CSV** para todos los modelos
- **CORS Habilitado** para aplicaciones frontend
- **Validación Robusta** de datos
- **Manejo de Errores Comprehensivo**

## 📦 Instalación

1. **Clonar el repositorio**
```bash
cd fenix
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus valores
```

5. **Configurar base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. **Ejecutar servidor**
```bash
python manage.py runserver
```

## 📚 Endpoints de la API

### 🏠 Root Endpoint
- **GET** `/` - Información de la API y lista de endpoints

### 🏷️ Categorías
- **GET** `/api/categories/` - Listar categorías
- **POST** `/api/categories/` - Crear categoría
- **GET** `/api/categories/{id}/` - Detalle de categoría (con productos anidados)
- **PUT/PATCH** `/api/categories/{id}/` - Actualizar categoría
- **DELETE** `/api/categories/{id}/` - Eliminar categoría

**Filtros disponibles:**
- `?search=nombre` - Buscar en nombre y descripción
- `?ordering=name,-id` - Ordenar por campos

### 👕 Productos
- **GET** `/api/products/` - Listar productos
- **POST** `/api/products/` - Crear producto
- **GET** `/api/products/{id}/` - Detalle de producto
- **PUT/PATCH** `/api/products/{id}/` - Actualizar producto
- **DELETE** `/api/products/{id}/` - Eliminar producto
- **GET** `/api/products/export-csv/` - Exportar productos a CSV

**Filtros disponibles:**
- `?search=nombre` - Buscar en nombre
- `?category=1` - Filtrar por categoría
- `?size=M` - Filtrar por talla exacta
- `?size__icontains=m` - Filtrar por talla que contenga
- `?color=azul` - Filtrar por color exacto
- `?color__icontains=az` - Filtrar por color que contenga
- `?price_min=10&price_max=100` - Rango de precios
- `?stock_min=5` - Stock mínimo
- `?ordering=price,-created_at` - Ordenar por campos

### 👥 Clientes
- **GET** `/api/customers/` - Listar clientes
- **POST** `/api/customers/` - Crear cliente
- **GET** `/api/customers/{id}/` - Detalle de cliente
- **PUT/PATCH** `/api/customers/{id}/` - Actualizar cliente
- **DELETE** `/api/customers/{id}/` - Eliminar cliente
- **GET** `/api/customers/export-csv/` - Exportar clientes a CSV

**Filtros disponibles:**
- `?search=nombre` - Buscar en nombre y email
- `?ordering=name,-created_at` - Ordenar por campos

### 🛒 Pedidos
- **GET** `/api/orders/` - Listar pedidos
- **POST** `/api/orders/` - Crear pedido (con items anidados)
- **GET** `/api/orders/{id}/` - Detalle de pedido
- **PUT/PATCH** `/api/orders/{id}/` - Actualizar pedido
- **DELETE** `/api/orders/{id}/` - Eliminar pedido
- **GET** `/api/orders/export-csv/` - Exportar pedidos a CSV

**Filtros disponibles:**
- `?customer=1` - Filtrar por cliente
- `?status=PENDIENTE` - Filtrar por estado
- `?order_date_from=2023-01-01&order_date_to=2023-12-31` - Rango de fechas
- `?total_min=100&total_max=500` - Rango de totales
- `?ordering=-order_date` - Ordenar por campos

### 📦 Items de Pedido
- **GET** `/api/order-items/` - Listar items
- **POST** `/api/order-items/` - Crear item
- **GET** `/api/order-items/{id}/` - Detalle de item
- **PUT/PATCH** `/api/order-items/{id}/` - Actualizar item
- **DELETE** `/api/order-items/{id}/` - Eliminar item
- **GET** `/api/order-items/export-csv/` - Exportar items a CSV

**Filtros disponibles:**
- `?order=1` - Filtrar por pedido
- `?product=1` - Filtrar por producto

## 📝 Ejemplos de Uso

### Crear un pedido con items anidados
```json
POST /api/orders/
{
    "customer": 1,
    "items": [
        {
            "product": 1,
            "quantity": 2
        },
        {
            "product": 2,
            "quantity": 1
        }
    ]
}
```

### Crear un producto
```json
POST /api/products/
{
    "name": "Camiseta Azul",
    "size": "M",
    "color": "Azul",
    "price": "25.99",
    "stock": 100,
    "category": 1
}
```

### Filtrar productos por rango de precio y categoría
```
GET /api/products/?category=1&price_min=10&price_max=50&ordering=price
```

### Buscar clientes por nombre
```
GET /api/customers/?search=juan&ordering=name
```

## 🔧 Configuración Avanzada

### Paginación
Por defecto, la API pagina los resultados a 20 elementos por página. Puedes navegar usando:
- `?page=2` - Página específica
- Los headers `Link` incluyen URLs para `next`, `previous`, `first` y `last`

### CORS
Para aplicaciones frontend, configura los orígenes permitidos en `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React
    "http://localhost:8080",  # Vue.js
]
```

### Base de Datos
La aplicación está configurada para PostgreSQL. Para usar SQLite en desarrollo:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## 🚦 Estados de Respuesta

- **200 OK** - Operación exitosa
- **201 Created** - Recurso creado exitosamente
- **204 No Content** - Eliminación exitosa
- **400 Bad Request** - Datos inválidos
- **404 Not Found** - Recurso no encontrado
- **409 Conflict** - Conflicto (ej: nombre duplicado)
- **500 Internal Server Error** - Error del servidor

## 🔍 Logging

La aplicación incluye logging configurado para desarrollo. Los logs se muestran en la consola con información sobre:
- Operaciones CRUD
- Errores de validación
- Accesos a endpoints
- Errores del sistema

## 🧪 Testing

Para ejecutar las pruebas:
```bash
python manage.py test
```

## 📈 Próximas Funcionalidades

- [ ] Autenticación JWT
- [ ] Roles y permisos
- [ ] Webhook notifications
- [ ] API versioning
- [ ] Rate limiting
- [ ] Métricas y analytics
- [ ] Documentación interactiva con Swagger

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu funcionalidad (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para más detalles.
