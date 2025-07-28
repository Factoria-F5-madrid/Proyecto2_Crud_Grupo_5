import axios from 'axios';

// Configuración base de axios
const api = axios.create({
  baseURL: 'https://fenix-backend.onrender.com/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para requests
api.interceptors.request.use(
  (config) => {
    // Agregar token de autenticación si existe
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para responses
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Manejar errores de autenticación
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API Services

// Categorías
export const categoryAPI = {
  getAll: () => api.get('/categories/'),
  getById: (id) => api.get(`/categories/${id}/`),
  create: (data) => api.post('/categories/', data),
  update: (id, data) => api.put(`/categories/${id}/`, data),
  partialUpdate: (id, data) => api.patch(`/categories/${id}/`, data),
  delete: (id) => api.delete(`/categories/${id}/`),
};

// Productos
export const productAPI = {
  getAll: (params = {}) => api.get('/products/', { params }),
  getById: (id) => api.get(`/products/${id}/`),
  create: (data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key]);
      }
    });
    return api.post('/products/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  update: (id, data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key]);
      }
    });
    return api.put(`/products/${id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  partialUpdate: (id, data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key]);
      }
    });
    return api.patch(`/products/${id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  delete: (id) => api.delete(`/products/${id}/`),
  exportCSV: () => api.get('/products/export-csv/', { responseType: 'blob' }),
};

// Clientes
export const customerAPI = {
  getAll: (params = {}) => api.get('/customers/', { params }),
  getById: (id) => api.get(`/customers/${id}/`),
  create: (data) => api.post('/customers/', data),
  update: (id, data) => api.put(`/customers/${id}/`, data),
  partialUpdate: (id, data) => api.patch(`/customers/${id}/`, data),
  delete: (id) => api.delete(`/customers/${id}/`),
  exportCSV: () => api.get('/customers/export-csv/', { responseType: 'blob' }),
};

// Usuarias
export const usuariaAPI = {
  getAll: (params = {}) => api.get('/usuarias/', { params }),
  getById: (id) => api.get(`/usuarias/${id}/`),
  create: (data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key]);
      }
    });
    return api.post('/usuarias/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  update: (id, data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key]);
      }
    });
    return api.put(`/usuarias/${id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  partialUpdate: (id, data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key]);
      }
    });
    return api.patch(`/usuarias/${id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  delete: (id) => api.delete(`/usuarias/${id}/`),
  reactivate: (id) => api.post(`/usuarias/${id}/reactivate/`),
  getStatistics: () => api.get('/usuarias/statistics/'),
  exportCSV: () => api.get('/usuarias/export-csv/', { responseType: 'blob' }),
};

// Pedidos (Orders)
export const orderAPI = {
  getAll: (params = {}) => api.get('/orders/', { params }),
  getById: (id) => api.get(`/orders/${id}/`),
  create: (data) => api.post('/orders/', data),
  update: (id, data) => api.put(`/orders/${id}/`, data),
  partialUpdate: (id, data) => api.patch(`/orders/${id}/`, data),
  delete: (id) => api.delete(`/orders/${id}/`),
  exportCSV: () => api.get('/orders/export-csv/', { responseType: 'blob' }),
};

// Items de pedido
export const orderItemAPI = {
  getAll: (params = {}) => api.get('/order-items/', { params }),
  getById: (id) => api.get(`/order-items/${id}/`),
  create: (data) => api.post('/order-items/', data),
  update: (id, data) => api.put(`/order-items/${id}/`, data),
  partialUpdate: (id, data) => api.patch(`/order-items/${id}/`, data),
  delete: (id) => api.delete(`/order-items/${id}/`),
  exportCSV: () => api.get('/order-items/export-csv/', { responseType: 'blob' }),
};

// Utilidades para manejo de archivos
export const downloadFile = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

// Utilidades para manejo de errores
export const handleAPIError = (error) => {
  if (error.response) {
    // Error de respuesta del servidor
    const status = error.response.status;
    const data = error.response.data;
    
    switch (status) {
      case 400:
        return { type: 'validation', message: 'Datos inválidos', details: data };
      case 401:
        return { type: 'auth', message: 'No autorizado' };
      case 403:
        return { type: 'permission', message: 'Sin permisos' };
      case 404:
        return { type: 'notfound', message: 'Recurso no encontrado' };
      case 409:
        return { type: 'conflict', message: 'Conflicto en los datos' };
      case 500:
        return { type: 'server', message: 'Error interno del servidor' };
      default:
        return { type: 'unknown', message: 'Error desconocido' };
    }
  } else if (error.request) {
    // Error de red
    return { type: 'network', message: 'Error de conexión' };
  } else {
    // Error de configuración
    return { type: 'config', message: 'Error de configuración' };
  }
};

export default api;
