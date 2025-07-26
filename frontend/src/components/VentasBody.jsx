import { useState, useEffect } from 'react';
import { orderAPI, customerAPI, usuariaAPI, productAPI, handleAPIError, downloadFile } from '../services/api';

export default function VentasBody() {
  const [ventas, setVentas] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [usuarias, setUsuarias] = useState([]);
  const [prendas, setPrendas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingVenta, setEditingVenta] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  // Formulario para nueva venta
  const [formData, setFormData] = useState({
    usuaria: '',
    customer: '',
    product: '',
    quantity: '1',
    total: '',
    date: new Date().toISOString().split('T')[0], // Fecha actual por defecto
  });

  useEffect(() => {
    fetchVentas();
    fetchClientes();
    fetchUsuarias();
    fetchPrendas();
  }, []);

  const fetchVentas = async () => {
    try {
      setLoading(true);
      const params = searchTerm ? { search: searchTerm } : {};
      const response = await orderAPI.getAll(params);
      setVentas(response.data.results || response.data);
      setError(null);
    } catch (err) {
      const errorInfo = handleAPIError(err);
      setError(errorInfo.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchClientes = async () => {
    try {
      const response = await customerAPI.getAll();
      setClientes(response.data.results || response.data);
    } catch (err) {
      console.error('Error fetching customers:', err);
    }
  };

  const fetchUsuarias = async () => {
    try {
      console.log('Fetching usuarias...');
      const response = await usuariaAPI.getAll();
      console.log('Usuarias response:', response);
      const usuariasData = response.data.results || response.data;
      console.log('Usuarias data:', usuariasData);
      setUsuarias(usuariasData);
    } catch (err) {
      console.error('Error fetching usuarias:', err);
    }
  };

  const fetchPrendas = async () => {
    try {
      console.log('Fetching prendas...');
      const response = await productAPI.getAll();
      console.log('Prendas response:', response);
      const prendasData = response.data.results || response.data;
      console.log('Prendas data:', prendasData);
      setPrendas(prendasData);
    } catch (err) {
      console.error('Error fetching prendas:', err);
    }
  };

  // Manejador cambio inputs
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // Resetear formulario
  const resetForm = () => {
    setFormData({
      usuaria: '',
      customer: '',
      product: '',
      quantity: '1',
      total: '',
      date: new Date().toISOString().split('T')[0],
    });
    setEditingVenta(null);
  };

  // Crear o actualizar venta
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const ventaData = {
        usuaria: parseInt(formData.usuaria),
        customer: parseInt(formData.customer),
        product: parseInt(formData.product),
        quantity: parseInt(formData.quantity),
        total: parseFloat(formData.total),
        date: formData.date,
      };

      if (editingVenta) {
        await orderAPI.partialUpdate(editingVenta.id, ventaData);
      } else {
        await orderAPI.create(ventaData);
      }
      resetForm();
      fetchVentas();
    } catch (err) {
      const errorInfo = handleAPIError(err);
      alert(errorInfo.message);
    }
  };

  // Editar venta
  const handleEdit = (venta) => {
    setFormData({
      usuaria: venta.usuaria?.id?.toString() || '',
      customer: venta.customer?.id?.toString() || '',
      product: venta.product?.id?.toString() || '',
      quantity: venta.quantity?.toString() || '1',
      total: venta.total.toString(),
      date: venta.date,
    });
    setEditingVenta(venta);
  };

  // Eliminar venta
  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar esta venta?')) {
      try {
        await orderAPI.delete(id);
        fetchVentas();
      } catch (err) {
        const errorInfo = handleAPIError(err);
        alert(errorInfo.message);
      }
    }
  };

  const handleExportCSV = async () => {
    try {
      const response = await orderAPI.exportCSV();
      downloadFile(response.data, 'ventas.csv');
    } catch (err) {
      const errorInfo = handleAPIError(err);
      alert(errorInfo.message);
    }
  };

  if (loading) return <p className="p-6">Cargando ventas...</p>;
  if (error) return <p className="p-6 text-red-600">{error}</p>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Gestión de Ventas</h1>
        <button 
          onClick={handleExportCSV}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Exportar CSV
        </button>
      </div>

      {/* Búsqueda */}
      <div className="mb-6 p-4 border rounded shadow bg-gray-50">
        <div className="flex gap-4">
          <input
            type="text"
            placeholder="Buscar ventas..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 p-2 border rounded"
          />
          <button 
            onClick={fetchVentas}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Buscar
          </button>
          <button 
            onClick={() => {
              setSearchTerm('');
              fetchVentas();
            }}
            className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
          >
            Limpiar
          </button>
        </div>
      </div>

      {/* Formulario */}
      <form onSubmit={handleSubmit} className="mb-8 max-w-md border p-4 rounded shadow">
        <h2 className="text-xl mb-4 font-semibold">
          {editingVenta ? 'Editar Venta' : 'Nueva Venta'}
        </h2>

        <select
          name="usuaria"
          value={formData.usuaria}
          onChange={handleChange}
          required
          className="w-full mb-2 p-2 border rounded"
        >
          <option value="">Seleccionar Usuaria</option>
          {usuarias.map(usuaria => (
            <option key={usuaria.id} value={usuaria.id}>
              {usuaria.full_name || `${usuaria.first_name} ${usuaria.last_name}`}
            </option>
          ))}
        </select>

        <select
          name="customer"
          value={formData.customer}
          onChange={handleChange}
          required
          className="w-full mb-2 p-2 border rounded"
        >
          <option value="">Seleccionar Cliente</option>
          {clientes.map(cliente => (
            <option key={cliente.id} value={cliente.id}>
              {cliente.name}
            </option>
          ))}
        </select>

        <select
          name="product"
          value={formData.product}
          onChange={handleChange}
          required
          className="w-full mb-2 p-2 border rounded"
        >
          <option value="">Seleccionar Prenda</option>
          {prendas.map(prenda => (
            <option key={prenda.id} value={prenda.id}>
              {prenda.name} - ${prenda.price}
            </option>
          ))}
        </select>

        <input
          type="number"
          name="quantity"
          placeholder="Cantidad"
          value={formData.quantity}
          onChange={handleChange}
          required
          min="1"
          className="w-full mb-2 p-2 border rounded"
        />

        <input
          type="number"
          name="total"
          placeholder="Total de la venta"
          value={formData.total}
          onChange={handleChange}
          required
          min="0"
          step="0.01"
          className="w-full mb-2 p-2 border rounded"
        />

        <input
          type="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
          required
          className="w-full mb-4 p-2 border rounded"
        />

        <div className="flex gap-2">
          <button type="submit" className="bg-pink-600 text-white py-2 px-4 rounded hover:bg-pink-700">
            {editingVenta ? 'Actualizar' : 'Crear'} Venta
          </button>
          {editingVenta && (
            <button 
              type="button"
              onClick={resetForm}
              className="bg-gray-600 text-white py-2 px-4 rounded hover:bg-gray-700"
            >
              Cancelar
            </button>
          )}
        </div>
      </form>

      {/* Lista de ventas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {ventas.map((venta) => (
          <div key={venta.id} className="border p-4 rounded shadow">
            <h3 className="text-lg font-semibold mb-2">Venta #{venta.id}</h3>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Usuaria:</span> {venta.usuaria?.name || 'N/A'}
            </p>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Cliente:</span> {venta.customer?.name || 'N/A'}
            </p>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Prenda:</span> {venta.product?.name || 'N/A'}
            </p>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Cantidad:</span> {venta.quantity || 1}
            </p>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Total:</span> ${parseFloat(venta.total).toFixed(2)}
            </p>
            <p className="text-gray-500 text-sm mb-4">
              <span className="font-medium">Fecha:</span> {new Date(venta.date).toLocaleDateString()}
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => handleEdit(venta)}
                className="flex-1 bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
              >
                Editar
              </button>
              <button
                onClick={() => handleDelete(venta.id)}
                className="flex-1 bg-red-600 text-white py-2 px-4 rounded hover:bg-red-700"
              >
                Eliminar
              </button>
            </div>
          </div>
        ))}
      </div>

      {ventas.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No hay ventas registradas.
        </div>
      )}
    </div>
  );
}
