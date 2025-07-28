import React, { useState, useEffect } from "react";
import { FaPlus, FaEdit, FaTrash, FaEye, FaTimes } from "react-icons/fa";
import { orderAPI, customerAPI, productAPI, usuariaAPI, orderItemAPI, handleAPIError } from '../services/api';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const VentasApp = () => {
  const [orders, setOrders] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);
  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [editingOrder, setEditingOrder] = useState(null);
  const [orderData, setOrderData] = useState({
    customer: '',
    usuaria: '',
    reservationDate: '',
    deliveryDate: '',
    orderDate: new Date().toISOString().split('T')[0],
    totalAmount: '',
    product: '',
    quantity: '1'
  });

  useEffect(() => {
    fetchOrders();
    fetchCustomers();
    fetchProducts();
    fetchUsers();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await productAPI.getAll();
      setProducts(response.data.results || response.data);
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(`Error al cargar productos: ${errorInfo.message}`);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await usuariaAPI.getAll();
      setUsers(response.data.results || response.data);
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(`Error al cargar usuarias: ${errorInfo.message}`);
    }
  };

  const fetchOrders = async () => {
    try {
      setIsLoading(true);
      const response = await orderAPI.getAll();
      // Forzar una nueva referencia del array para garantizar re-renderizado
      const ordersData = response.data.results || response.data;
      setOrders([...ordersData]);
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(`Error al cargar las órdenes: ${errorInfo.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchCustomers = async () => {
    try {
      const response = await customerAPI.getAll();
      setCustomers(response.data.results || response.data);
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(`Error al cargar clientes: ${errorInfo.message}`);
    }
  };

  const handleAdd = () => {
    resetForm(); // Limpiar formulario al abrir
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    resetForm(); // Limpiar formulario al cerrar
  };

  const resetForm = () => {
    setOrderData({
      customer: '',
      usuaria: '',
      reservationDate: '',
      deliveryDate: '',
      orderDate: new Date().toISOString().split('T')[0],
      totalAmount: '',
      product: '',
      quantity: '1'
    });
  };

  const calculateTotal = (productId, quantity) => {
    const product = products.find(p => p.id === parseInt(productId));
    if (product && quantity) {
      const total = parseFloat(product.price) * parseInt(quantity);
      return total.toFixed(2);
    }
    return '';
  };

  const validateForm = (isEditing = false) => {
    const errors = [];
    
    // Validaciones requeridas
    if (!orderData.customer) errors.push('Debe seleccionar un cliente');
    // Solo requerir usuaria para nuevas órdenes, no para ediciones
    if (!orderData.orderDate) errors.push('Debe ingresar la fecha de la orden');
    if (!orderData.product) errors.push('Debe seleccionar una prenda');
    if (!orderData.quantity || parseInt(orderData.quantity) < 1) errors.push('Debe ingresar una cantidad válida');
    if (!orderData.totalAmount || parseFloat(orderData.totalAmount) <= 0) errors.push('Debe ingresar un precio total válido');
    
    // Validaciones de fechas
    if (orderData.reservationDate && orderData.deliveryDate) {
      if (new Date(orderData.deliveryDate) < new Date(orderData.reservationDate)) {
        errors.push('La fecha de entrega debe ser posterior a la fecha de reserva');
      }
    }
    
    if (orderData.reservationDate && new Date(orderData.reservationDate) < new Date(orderData.orderDate)) {
      errors.push('La fecha de reserva no puede ser anterior a la fecha de la orden');
    }
    
    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validar formulario
    const validationErrors = validateForm();
    if (validationErrors.length > 0) {
      validationErrors.forEach(error => toast.error(error));
      return;
    }
    
    try {
      // Preparar datos según la estructura que espera el backend
      // El backend espera una orden con items anidados
      const orderPayload = {
        customer: parseInt(orderData.customer),
        items: [
          {
            product: parseInt(orderData.product),
            quantity: parseInt(orderData.quantity),
            price: parseFloat(orderData.totalAmount) / parseInt(orderData.quantity)
          }
        ]
      };
      
      console.log('Enviando datos de orden:', orderPayload);
      
      // Crear la orden con items anidados
      const orderResponse = await orderAPI.create(orderPayload);
      
      console.log('Respuesta de la API:', orderResponse);
      
      toast.success('¡Venta registrada exitosamente!');
      setIsModalOpen(false);
      resetForm();
      await fetchOrders(); // Recargar la lista
      
    } catch (error) {
      console.error('Error completo:', error);
      console.error('Error response:', error.response);
      console.error('Error data:', error.response?.data);
      
      let errorMessage = 'Error desconocido';
      
      if (error.response?.data) {
        // Si hay errores específicos de validación
        if (typeof error.response.data === 'object') {
          const errors = [];
          Object.keys(error.response.data).forEach(key => {
            if (Array.isArray(error.response.data[key])) {
              errors.push(`${key}: ${error.response.data[key].join(', ')}`);
            } else {
              errors.push(`${key}: ${error.response.data[key]}`);
            }
          });
          errorMessage = errors.join('; ');
        } else {
          errorMessage = error.response.data.toString();
        }
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      toast.error(`Error al registrar la venta: ${errorMessage}`);
    }
  };

  const handleView = (order) => {
    setSelectedOrder(order);
  };

  const handleUpdate = async (order) => {
    try {
      // Buscar los detalles completos de la orden si no los tenemos
      let fullOrder = order;
      if (!order.items || order.items.length === 0) {
        const response = await orderAPI.getById(order.id);
        fullOrder = response.data;
      }
      
      // Preparar datos para edición basados en la orden existente
      if (fullOrder.items && fullOrder.items.length > 0) {
        const firstItem = fullOrder.items[0]; // Asumimos un item por orden para simplificar
        setOrderData({
          customer: fullOrder.customer.toString(),
          usuaria: '', // Este campo no se guarda en el backend actualmente
          reservationDate: '',
          deliveryDate: '',
          orderDate: fullOrder.order_date ? fullOrder.order_date.split('T')[0] : new Date().toISOString().split('T')[0],
          totalAmount: fullOrder.total_amount.toString(),
          product: firstItem.product.toString(),
          quantity: firstItem.quantity.toString()
        });
      } else {
        // Si no hay items, usar valores por defecto
        setOrderData({
          customer: fullOrder.customer.toString(),
          usuaria: '',
          reservationDate: '',
          deliveryDate: '',
          orderDate: fullOrder.order_date ? fullOrder.order_date.split('T')[0] : new Date().toISOString().split('T')[0],
          totalAmount: fullOrder.total_amount.toString(),
          product: '',
          quantity: '1'
        });
      }
      
      setEditingOrder(fullOrder);
      setIsEditModalOpen(true);
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(`Error al cargar la orden: ${errorInfo.message}`);
    }
  };
  
  const handleQuickStatusUpdate = async (orderId, newStatus) => {
    try {
await orderAPI.partialUpdate(orderId, { status: newStatus });
      toast.success(`Estado actualizado a ${getStatusText(newStatus)}`);
      setOrders(prevOrders => 
        prevOrders.map(order => 
          order.id === orderId ? {...order, status: newStatus} : order
        )
      );
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(`Error al actualizar estado: ${errorInfo.message}`);
    }
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    
    // Validar formulario
    const validationErrors = validateForm();
    if (validationErrors.length > 0) {
      validationErrors.forEach(error => toast.error(error));
      return;
    }
    
    try {
      // Preparar datos para actualización
      const updatePayload = {
        customer: parseInt(orderData.customer),
        status: editingOrder.status,
        total_amount: parseFloat(orderData.totalAmount),
        items: [
          {
            product: parseInt(orderData.product),
            quantity: parseInt(orderData.quantity),
            price: parseFloat(orderData.totalAmount) / parseInt(orderData.quantity)
          }
        ]
      };
      
      console.log('Actualizando orden con datos:', updatePayload);
      
      // Actualizar la orden
      await orderAPI.update(editingOrder.id, updatePayload);
      
      toast.success('¡Orden actualizada exitosamente!');
      setIsEditModalOpen(false);
      setEditingOrder(null);
      resetForm();
      await fetchOrders(); // Recargar la lista
      
    } catch (error) {
      console.error('Error al actualizar orden:', error);
      console.error('Error response:', error.response);
      console.error('Error data:', error.response?.data);
      
      let errorMessage = 'Error desconocido';
      
      if (error.response?.data) {
        // Si hay errores específicos de validación
        if (typeof error.response.data === 'object') {
          const errors = [];
          Object.keys(error.response.data).forEach(key => {
            if (Array.isArray(error.response.data[key])) {
              errors.push(`${key}: ${error.response.data[key].join(', ')}`);
            } else {
              errors.push(`${key}: ${error.response.data[key]}`);
            }
          });
          errorMessage = errors.join('; ');
        } else {
          errorMessage = error.response.data.toString();
        }
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      toast.error(`Error al actualizar la orden: ${errorMessage}`);
    }
  };
  
  const getStatusText = (status) => {
    const statusMap = {
      'PENDIENTE': 'Pendiente',
      'PROCESANDO': 'Procesando', 
      'ENVIADO': 'Enviado',
      'COMPLETADO': 'Completado',
      'CANCELADO': 'Cancelado'
    };
    return statusMap[status] || status;
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar esta orden?')) {
      try {
        await orderAPI.delete(id);
        toast.success("Orden eliminada exitosamente");
        await fetchOrders();
      } catch (error) {
        const errorInfo = handleAPIError(error);
        toast.error(`Error al eliminar la orden: ${errorInfo.message}`);
      }
    }
  };

  const getCustomerName = (customerId) => {
    const customer = customers.find(c => c.id === customerId);
    return customer ? customer.name : 'Cliente no encontrado';
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      'PENDIENTE': { color: 'bg-yellow-100 text-yellow-800', text: 'Pendiente' },
      'PROCESANDO': { color: 'bg-blue-100 text-blue-800', text: 'Procesando' },
      'ENVIADO': { color: 'bg-purple-100 text-purple-800', text: 'Enviado' },
      'COMPLETADO': { color: 'bg-green-100 text-green-800', text: 'Completado' },
      'CANCELADO': { color: 'bg-red-100 text-red-800', text: 'Cancelado' }
    };
    
    const config = statusConfig[status] || { color: 'bg-gray-100 text-gray-800', text: status };
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color}`}>
        {config.text}
      </span>
    );
  };

  return (
    <div className="min-h-screen">
      <header >
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Gestión de Ventas</h1>
          <button
            onClick={handleAdd}
            className="flex items-center px-4 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600 transition-colors duration-200"
          >
            <FaPlus className="mr-2" />
            Nueva Orden
          </button>
        </div>

        {isLoading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
          </div>
        ) : (
          <div className="bg-white shadow-md rounded-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      # Orden
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Cliente
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Fecha
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Total
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Estado
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Acciones
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {orders.length === 0 ? (
                    <tr>
                      <td colSpan="6" className="px-6 py-8 text-center text-gray-500">
                        No hay órdenes registradas
                      </td>
                    </tr>
                  ) : (
                    orders.map((order) => (
                      <tr key={order.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          #{order.id}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {getCustomerName(order.customer)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {new Date(order.order_date).toLocaleDateString('es-ES')}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">
                          ${parseFloat(order.total_amount).toFixed(2)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center space-x-2">
                            {getStatusBadge(order.status)}
                            {order.status !== 'COMPLETADO' && order.status !== 'CANCELADO' && (
                              <select
                                value={order.status}
                                onChange={(e) => handleQuickStatusUpdate(order.id, e.target.value)}
                                className="text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-orange-500"
                                title="Cambiar estado rápidamente"
                              >
                                <option value="PENDIENTE">Pendiente</option>
                                <option value="PROCESANDO">Procesando</option>
                                <option value="ENVIADO">Enviado</option>
                                <option value="COMPLETADO">Completado</option>
                                <option value="CANCELADO">Cancelado</option>
                              </select>
                            )}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <div className="flex space-x-2">
                            <button
                              onClick={() => handleView(order)}
                              className="inline-flex items-center px-3 py-1 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors duration-200"
                              title="Ver detalles"
                            >
                              <FaEye className="mr-1" />
                              Ver
                            </button>
                            <button
                              onClick={() => handleUpdate(order)}
                              className="inline-flex items-center px-3 py-1 bg-orange-500 text-white rounded-md hover:bg-orange-600 transition-colors duration-200"
                              title="Editar orden"
                            >
                              <FaEdit className="mr-1" />
                              Editar
                            </button>
                            <button
                              onClick={() => handleDelete(order.id)}
                              className="inline-flex items-center px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors duration-200"
                              title="Eliminar orden"
                            >
                              <FaTrash className="mr-1" />
                              Eliminar
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>

      {/* Modal para crear nueva orden */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold text-gray-900">Registrar Nueva Venta</h3>
              <button
                onClick={handleCloseModal}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <FaTimes className="text-xl" />
              </button>
            </div>
            
            <form className="space-y-6" onSubmit={handleSubmit}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Cliente */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Nombre del Cliente *
                  </label>
                  <select
                    value={orderData.customer}
                    onChange={(e) => setOrderData({...orderData, customer: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    required
                  >
                    <option value="">Seleccione un cliente</option>
                    {customers.map(customer => (
                      <option key={customer.id} value={customer.id}>
                        {customer.name}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Usuaria que hizo la venta */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Usuaria que registra la venta *
                  </label>
<select
                    value={orderData.usuaria}
                    onChange={(e) => setOrderData({...orderData, usuaria: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  >
                    <option value="">Seleccione una usuaria</option>
                    {users.map(user => (
                      <option key={user.id} value={user.id}>
                        {user.first_name} {user.last_name} ({user.username})
                      </option>
                    ))}
                  </select>
                </div>

                {/* Día de reserva */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Día de Reserva
                  </label>
                  <input
                    type="date"
                    value={orderData.reservationDate}
                    onChange={(e) => setOrderData({...orderData, reservationDate: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  />
                </div>

                {/* Día de entrega */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Día de Entrega
                  </label>
                  <input
                    type="date"
                    value={orderData.deliveryDate}
                    onChange={(e) => setOrderData({...orderData, deliveryDate: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  />
                </div>

                {/* Fecha de la orden */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Fecha de la Orden *
                  </label>
                  <input
                    type="date"
                    value={orderData.orderDate}
                    onChange={(e) => setOrderData({...orderData, orderDate: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    required
                  />
                </div>

                {/* Prenda */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Prenda *
                  </label>
                  <select
                    value={orderData.product}
                    onChange={(e) => {
                      const newProduct = e.target.value;
                      const calculatedTotal = calculateTotal(newProduct, orderData.quantity);
                      setOrderData({
                        ...orderData, 
                        product: newProduct,
                        totalAmount: calculatedTotal
                      });
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    required
                  >
                    <option value="">Seleccione una prenda</option>
                    {products.map(product => (
                      <option key={product.id} value={product.id}>
                        {product.name} - ${parseFloat(product.price).toFixed(2)}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Unidades */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Unidades *
                  </label>
                  <input
                    type="number"
                    min="1"
                    value={orderData.quantity}
                    onChange={(e) => {
                      const newQuantity = e.target.value;
                      const calculatedTotal = calculateTotal(orderData.product, newQuantity);
                      setOrderData({
                        ...orderData, 
                        quantity: newQuantity,
                        totalAmount: calculatedTotal
                      });
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    required
                  />
                </div>

                {/* Precio total */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Precio Total ($) *
                    <span className="text-xs text-gray-500 font-normal ml-1">
                      (Se calcula automáticamente)
                    </span>
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    value={orderData.totalAmount}
                    onChange={(e) => setOrderData({...orderData, totalAmount: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-gray-50"
                    placeholder="0.00"
                    required
                    readOnly
                  />
                  {orderData.product && orderData.quantity && (
                    <p className="text-xs text-gray-600 mt-1">
                      Cálculo: {products.find(p => p.id === parseInt(orderData.product))?.name} 
                      × {orderData.quantity} unidades = ${orderData.totalAmount}
                    </p>
                  )}
                </div>
              </div>

              {/* Botones de acción */}
              <div className="flex justify-end space-x-4 pt-6 border-t border-gray-200">
                <button
                  type="button"
                  onClick={handleCloseModal}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-sm font-medium text-white bg-orange-500 border border-transparent rounded-md hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 transition-colors"
                >
                  Registrar Venta
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal para ver detalles de orden */}
      {selectedOrder && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">Detalles de la Orden #{selectedOrder.id}</h3>
              <button
                onClick={() => setSelectedOrder(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                ×
              </button>
            </div>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Cliente</label>
                  <p className="mt-1 text-sm text-gray-900">{getCustomerName(selectedOrder.customer)}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Fecha</label>
                  <p className="mt-1 text-sm text-gray-900">
                    {new Date(selectedOrder.order_date).toLocaleString('es-ES')}
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Estado</label>
                  <div className="mt-1">{getStatusBadge(selectedOrder.status)}</div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Total</label>
                  <p className="mt-1 text-sm text-gray-900 font-medium">
                    ${parseFloat(selectedOrder.total_amount).toFixed(2)}
                  </p>
                </div>
              </div>
              {selectedOrder.items && selectedOrder.items.length > 0 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Productos</label>
                  <div className="border rounded-md">
                    <table className="min-w-full">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Producto</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Cantidad</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Precio</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Total</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200">
                        {selectedOrder.items.map((item, index) => (
                          <tr key={index}>
                            <td className="px-4 py-2 text-sm text-gray-900">{item.product_name || item.product}</td>
                            <td className="px-4 py-2 text-sm text-gray-900">{item.quantity}</td>
                            <td className="px-4 py-2 text-sm text-gray-900">${parseFloat(item.price).toFixed(2)}</td>
                            <td className="px-4 py-2 text-sm text-gray-900">
                              ${(parseFloat(item.price) * item.quantity).toFixed(2)}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
            <div className="flex justify-end mt-6">
              <button
                onClick={() => setSelectedOrder(null)}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal para editar orden */}
      {isEditModalOpen && editingOrder && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold text-gray-900">Editar Orden #{editingOrder.id}</h3>
              <button
                onClick={() => {
                  setIsEditModalOpen(false);
                  setEditingOrder(null);
                  resetForm();
                }}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <FaTimes className="text-xl" />
              </button>
            </div>
            
            <form className="space-y-6" onSubmit={handleEditSubmit}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Cliente */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Nombre del Cliente *
                  </label>
                  <select
                    value={orderData.customer}
                    onChange={(e) => setOrderData({...orderData, customer: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    required
                  >
                    <option value="">Seleccione un cliente</option>
                    {customers.map(customer => (
                      <option key={customer.id} value={customer.id}>
                        {customer.name}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Estado */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Estado de la Orden *
                  </label>
                  <select
                    value={orderData.status || editingOrder.status}
                    onChange={(e) => {
                      const newStatus = e.target.value;
                      // Actualizar ambos estados para mantener sincronización
                      setEditingOrder({...editingOrder, status: newStatus});
                      setOrderData({...orderData, status: newStatus});
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    required
                  >
                    <option value="PENDIENTE">Pendiente</option>
                    <option value="PROCESANDO">Procesando</option>
                    <option value="ENVIADO">Enviado</option>
                    <option value="COMPLETADO">Completado</option>
                    <option value="CANCELADO">Cancelado</option>
                  </select>
                </div>

                {/* Prenda */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Prenda *
                  </label>
                  <select
                    value={orderData.product}
                    onChange={(e) => {
                      const newProduct = e.target.value;
                      const calculatedTotal = calculateTotal(newProduct, orderData.quantity);
                      setOrderData({
                        ...orderData, 
                        product: newProduct,
                        totalAmount: calculatedTotal
                      });
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    required
                  >
                    <option value="">Seleccione una prenda</option>
                    {products.map(product => (
                      <option key={product.id} value={product.id}>
                        {product.name} - ${parseFloat(product.price).toFixed(2)}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Unidades */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Unidades *
                  </label>
                  <input
                    type="number"
                    min="1"
                    value={orderData.quantity}
                    onChange={(e) => {
                      const newQuantity = e.target.value;
                      const calculatedTotal = calculateTotal(orderData.product, newQuantity);
                      setOrderData({
                        ...orderData, 
                        quantity: newQuantity,
                        totalAmount: calculatedTotal
                      });
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    required
                  />
                </div>

                {/* Precio total */}
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Precio Total ($) *
                    <span className="text-xs text-gray-500 font-normal ml-1">
                      (Se calcula automáticamente)
                    </span>
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    value={orderData.totalAmount}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-gray-50"
                    placeholder="0.00"
                    required
                    readOnly
                  />
                  {orderData.product && orderData.quantity && (
                    <p className="text-xs text-gray-600 mt-1">
                      Cálculo: {products.find(p => p.id === parseInt(orderData.product))?.name} 
                      × {orderData.quantity} unidades = ${orderData.totalAmount}
                    </p>
                  )}
                </div>
              </div>

              {/* Botones de acción */}
              <div className="flex justify-end space-x-4 pt-6 border-t border-gray-200">
                <button
                  type="button"
                  onClick={() => {
                    setIsEditModalOpen(false);
                    setEditingOrder(null);
                    resetForm();
                  }}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-sm font-medium text-white bg-orange-500 border border-transparent rounded-md hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 transition-colors"
                >
                  Actualizar Orden
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <ToastContainer position="bottom-right" />
    </div>
  );
};

export default VentasApp;
