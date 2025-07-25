# 🌐 Guía para Usar la Interfaz Web de Django REST Framework

## 🚀 ¡Problema Solucionado!

Ahora tu API tiene la **interfaz web navegable de Django REST Framework** completamente funcional. Ya no verás solo JSON, sino una interfaz completa para probar todos los endpoints.

## 📍 **URLs para Probar**

### **Página Principal**
```
http://localhost:8000/
```
- Lista todos los endpoints disponibles con enlaces clickeables

### **Endpoints Principales**
```bash
# Productos con imágenes
http://localhost:8000/api/products/          # Lista productos
http://localhost:8000/api/products/1/        # Detalle producto

# Categorías  
http://localhost:8000/api/categories/        # Lista categorías
http://localhost:8000/api/categories/1/      # Detalle categoría

# Clientes
http://localhost:8000/api/customers/         # Lista clientes
http://localhost:8000/api/customers/1/       # Detalle cliente

# Usuarias (NUEVO)
http://localhost:8000/api/usuarias/          # Lista usuarias
http://localhost:8000/api/usuarias/1/        # Detalle usuaria
http://localhost:8000/api/usuarias/statistics/ # Estadísticas

# Pedidos
http://localhost:8000/api/orders/            # Lista pedidos
http://localhost:8000/api/orders/1/          # Detalle pedido
```

## 🎯 **Cómo Probar los Endpoints**

### **1. Navegación Básica**
1. Ve a `http://localhost:8000/` - verás la página principal con enlaces
2. Haz clic en cualquier enlace para ir al endpoint
3. En cada endpoint verás:
   - **Formulario HTML** para hacer POST/PUT/PATCH
   - **Botones de acción** (GET, POST, OPTIONS)
   - **Filtros** disponibles en la URL

### **2. Crear un Producto CON IMAGEN**
1. Ve a `http://localhost:8000/api/products/`
2. Baja hasta el formulario HTML
3. Llena los campos:
   ```
   Name: "Mi Producto"
   Price: 25.99
   Stock: 100
   Category: 1
   Description: "Descripción del producto"
   Image: [SELECCIONAR ARCHIVO]
   ```
4. Haz clic en **POST**

### **3. Crear una Usuaria CON AVATAR**
1. Ve a `http://localhost:8000/api/usuarias/`
2. Llena el formulario:
   ```
   Username: "mi_usuario"
   Email: "mi@email.com"
   First name: "Mi Nombre"
   Last name: "Mi Apellido"
   Role: "EMPLOYEE"
   Avatar: [SELECCIONAR ARCHIVO]
   Password: "password123"
   Password confirm: "password123"
   ```
3. Haz clic en **POST**

### **4. Probar Filtros**
En la URL puedes agregar filtros directamente:
```bash
# Filtrar productos por categoría
http://localhost:8000/api/products/?category=1

# Buscar clientes
http://localhost:8000/api/customers/?search=juan

# Filtrar usuarias por rol
http://localhost:8000/api/usuarias/?role=ADMIN&is_active=true
```

### **5. Ver Estadísticas**
```bash
http://localhost:8000/api/usuarias/statistics/
```

## 🖼️ **Funcionalidades de Imágenes**

### **Productos**
- Campo `image` disponible en formularios
- URL completa de imagen en respuesta (`image_url`)
- Validación automática de archivos

### **Usuarias**
- Campo `avatar` para foto de perfil
- Mismas validaciones que productos

## 🎨 **Características de la Interfaz**

### **Lo que verás:**
- ✅ **Formularios HTML** para crear/editar
- ✅ **Botones de navegación** (GET, POST, OPTIONS)
- ✅ **Respuestas formateadas** en JSON bonito
- ✅ **Códigos de estado HTTP** coloreados
- ✅ **Filtros y paginación** funcionales
- ✅ **Breadcrumbs** de navegación
- ✅ **Documentación automática** de campos

### **Funciones Interactivas:**
- 🔍 **Explorar endpoints** haciendo clic
- 📝 **Crear datos** con formularios visuales
- ✏️ **Editar registros** existentes
- 🗑️ **Eliminar** (soft delete para usuarias)
- 📊 **Ver estadísticas** y reportes
- 💾 **Descargar CSV** directamente

## 🚦 **Datos de Muestra Disponibles**

Ya tienes datos creados para probar:
- **4 categorías**: Camisetas, Pantalones, Vestidos, Accesorios
- **5 productos**: Con diferentes categorías y precios
- **4 clientes**: Con emails y teléfonos
- **3 usuarias**: Admin, Employee, Manager con diferentes roles

## 🛠️ **Comandos Útiles**

```bash
# Iniciar servidor
python manage.py runserver

# Crear más datos de muestra
python create_sample_data.py

# Acceder al admin
http://localhost:8000/admin/
```

## 📱 **Pruebas Recomendadas**

### **1. Flujo Completo de Producto**
1. Crear categoría → Crear producto con imagen → Ver listado → Editar producto

### **2. Flujo de Usuarias** 
1. Crear usuaria → Ver estadísticas → Filtrar por rol → Desactivar → Reactivar

### **3. Pruebas de Filtros**
1. Filtrar productos por precio → Buscar clientes → Ordenar por fecha

### **4. Exportación**
1. Exportar productos a CSV → Exportar usuarias a CSV

## 🎉 **¡Todo Listo!**

Tu API ahora tiene:
- ✅ **Interfaz web completa** para pruebas
- ✅ **Soporte de imágenes** en productos y usuarias
- ✅ **CRUD completo** para todas las entidades
- ✅ **Filtros y búsqueda** avanzados
- ✅ **Datos de muestra** para probar
- ✅ **Validaciones robustas**
- ✅ **Exportación CSV**

**¡Empieza probando en http://localhost:8000/ ahora mismo!** 🚀
