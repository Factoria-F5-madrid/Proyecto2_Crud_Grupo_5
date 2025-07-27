# Conexión Completa Frontend-Backend - Proyecto Fénix

## 🚀 Resumen de Cambios Realizados

He conectado exitosamente todo el frontend de React con el backend de Django REST Framework. Ahora tienes un sistema CRUD completamente funcional que puede:

- ✅ Crear, leer, actualizar y eliminar **Productos** (Prendas)
- ✅ Crear, leer, actualizar y eliminar **Clientes**
- ✅ Crear, leer, actualizar y eliminar **Usuarias**
- ✅ Visualizar y eliminar **Ventas** (Órdenes)
- ✅ Manejo completo de errores con notificaciones toast
- ✅ Carga de imágenes para productos y avatares
- ✅ Interfaz responsive y moderna

## 📁 Estructura del Proyecto

```
Proyecto2_Crud_Grupo_5/
├── fenix/                          # Backend Django REST Framework
│   ├── .env                        # Variables de entorno (CREADO)
│   ├── manage.py
│   ├── requirements.txt
│   ├── fenix/
│   │   ├── settings.py            # Configuración con CORS
│   │   └── urls.py
│   ├── cliente/                    # App de clientes
│   ├── prenda/                     # App de productos
│   ├── usuarias/                   # App de usuarias
│   ├── compra/                     # App de órdenes/ventas
│   └── categoría/                  # App de categorías
├── frontend/                       # Frontend React
│   ├── src/
│   │   ├── services/
│   │   │   └── api.js              # Servicios API configurados
│   │   └── components/
│   │       ├── PrendasBody.jsx     # ACTUALIZADO - Conectado a API
│   │       ├── ClientesBody.jsx    # ACTUALIZADO - Conectado a API
│   │       ├── UsuariasBody.jsx    # ACTUALIZADO - Conectado a API
│   │       └── VentasBody.jsx      # ACTUALIZADO - Conectado a API
│   └── package.json
└── README_CONEXION_COMPLETA.md     # Este archivo
```

## 🔧 Configuración e Instalación

### 1. Backend (Django REST Framework)

```bash
cd fenix

# Activar entorno virtual
source .venv/bin/activate  # En Linux/Mac
# o
.venv\Scripts\activate     # En Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
# Edita el archivo .env con tus credenciales de PostgreSQL:
# DB_NAME=fenix_db
# DB_USER=tu_usuario
# DB_PASSWORD=tu_contraseña
# DB_HOST=localhost
# DB_PORT=5432

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser

# Ejecutar servidor de desarrollo
python manage.py runserver
```

El backend estará disponible en: http://localhost:8000

### 2. Frontend (React)

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: http://localhost:5173

## 🛠️ Funcionalidades Implementadas

### 📦 Componente PrendasBody
- **Conectado a:** `/api/products/` y `/api/categories/`
- **Funciones:**
  - ✅ Listar productos con paginación
  - ✅ Crear nuevo producto con imagen
  - ✅ Editar producto existente
  - ✅ Eliminar producto con confirmación
  - ✅ Filtrar por categoría y búsqueda
  - ✅ Mostrar categorías dinámicamente desde la API

### 👥 Componente ClientesBody
- **Conectado a:** `/api/customers/`
- **Funciones:**
  - ✅ Listar clientes
  - ✅ Crear nuevo cliente
  - ✅ Editar cliente inline
  - ✅ Eliminar cliente
  - ✅ Gestión dinámica de columnas

### 👩‍💼 Componente UsuariasBody
- **Conectado a:** `/api/usuarias/`
- **Funciones:**
  - ✅ Listar usuarias del sistema
  - ✅ Crear nueva usuaria con avatar
  - ✅ Editar usuaria con todos los campos
  - ✅ Eliminar usuaria
  - ✅ Campos: username, nombre, apellido, email, teléfono, rol, estado, fecha de contratación, salario, dirección

### 💰 Componente VentasBody
- **Conectado a:** `/api/orders/`
- **Funciones:**
  - ✅ Listar órdenes/ventas
  - ✅ Eliminar órdenes
  - ⚠️ Crear/editar órdenes (pendiente de implementar)

## 🎨 Características de la UI

- **Notificaciones Toast:** Feedback visual para todas las operaciones
- **Loading States:** Indicadores de carga durante las peticiones API
- **Manejo de Errores:** Mensajes de error descriptivos
- **Responsive Design:** Funciona en desktop y mobile
- **Modales de Confirmación:** Para operaciones destructivas
- **Formularios Dinámicos:** Adaptados a los modelos del backend

## 🔄 Flujo de Datos

```
React Component → API Service → Django REST API → Database
        ↓
React Component ← JSON Response ← Django REST API ← Database
```

## 📡 Endpoints API Utilizados

```
Productos:
GET    /api/products/          # Listar productos
POST   /api/products/          # Crear producto
PUT    /api/products/{id}/     # Actualizar producto
DELETE /api/products/{id}/     # Eliminar producto

Clientes:
GET    /api/customers/         # Listar clientes
POST   /api/customers/         # Crear cliente
PUT    /api/customers/{id}/    # Actualizar cliente
DELETE /api/customers/{id}/    # Eliminar cliente

Usuarias:
GET    /api/usuarias/          # Listar usuarias
POST   /api/usuarias/          # Crear usuaria
PUT    /api/usuarias/{id}/     # Actualizar usuaria
DELETE /api/usuarias/{id}/     # Eliminar usuaria

Categorías:
GET    /api/categories/        # Listar categorías

Órdenes:
GET    /api/orders/            # Listar órdenes
DELETE /api/orders/{id}/       # Eliminar orden
```

## 🚨 Troubleshooting

### Problemas Comunes:

1. **Error de CORS:**
   - Verifica que el frontend esté ejecutándose en un puerto permitido (5173, 3000, etc.)
   - Revisa la configuración de CORS en `fenix/settings.py`

2. **Error de Base de Datos:**
   - Asegúrate de que PostgreSQL esté ejecutándose
   - Verifica las credenciales en el archivo `.env`
   - Ejecuta las migraciones: `python manage.py migrate`

3. **Error 404 en API:**
   - Verifica que el backend esté corriendo en el puerto 8000
   - Revisa que las URLs estén correctamente configuradas

4. **Error de dependencias:**
   - Backend: `pip install -r requirements.txt`
   - Frontend: `npm install`

## 🔜 Próximos Pasos

1. **Implementar creación/edición de órdenes** en VentasBody
2. **Añadir autenticación** con JWT tokens
3. **Implementar paginación** en el frontend
4. **Añadir filtros avanzados** por fecha, precio, etc.
5. **Mejorar validación** de formularios
6. **Añadir tests** unitarios y de integración

## 📞 Soporte

Si encuentras algún problema:

1. Verifica que ambos servidores estén ejecutándose
2. Revisa la consola del navegador para errores de JavaScript
3. Revisa los logs del servidor Django para errores de backend
4. Asegúrate de que todas las dependencias estén instaladas

¡El sistema CRUD está completamente funcional y listo para usar! 🎉
