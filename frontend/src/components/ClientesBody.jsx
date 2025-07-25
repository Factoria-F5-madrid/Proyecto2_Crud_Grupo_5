import { useState, useEffect } from 'react';
import { customerAPI, handleAPIError, downloadFile } from '../services/api';

export default function ClientesBody() {
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingClient, setEditingClient] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  // Formulario para nuevo cliente
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
  });

  useEffect(() => {
    fetchClientes();
  }, []);

  const fetchClientes = async () => {
    try {
      setLoading(true);
      const params = searchTerm ? { search: searchTerm } : {};
      const response = await customerAPI.getAll(params);
      setClientes(response.data.results || response.data);
      setError(null);
    } catch (err) {
      const errorInfo = handleAPIError(err);
      setError(errorInfo.message);
    } finally {
      setLoading(false);
    }
  };

  // Manejador cambio inputs
  const handleChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // Resetear formulario
  const resetForm = () => {
    setFormData({ name: '', email: '', phone: '' });
    setEditingClient(null);
  };

  // Crear o actualizar cliente
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingClient) {
        await customerAPI.partialUpdate(editingClient.id, formData);
      } else {
        await customerAPI.create(formData);
      }
      resetForm();
      fetchClientes();
    } catch (err) {
      const errorInfo = handleAPIError(err);
      alert(errorInfo.message);
    }
  };

  // Editar cliente
  const handleEdit = (cliente) => {
    setFormData({
      name: cliente.name,
      email: cliente.email,
      phone: cliente.phone || '',
    });
    setEditingClient(cliente);
  };

  // Eliminar cliente
  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar este cliente?')) {
      try {
        await customerAPI.delete(id);
        fetchClientes();
      } catch (err) {
        const errorInfo = handleAPIError(err);
        alert(errorInfo.message);
      }
    }
  };

  // Exportar CSV
  const handleExportCSV = async () => {
    try {
      const response = await customerAPI.exportCSV();
      downloadFile(response.data, 'clientes.csv');
    } catch (err) {
      const errorInfo = handleAPIError(err);
      alert(errorInfo.message);
    }
  };

  if (loading) return <p className="p-6">Cargando clientes...</p>;
  if (error) return <p className="p-6 text-red-600">{error}</p>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Gestión de Clientes</h1>
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
            placeholder="Buscar clientes por nombre o email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 p-2 border rounded"
          />
          <button 
            onClick={fetchClientes}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Buscar
          </button>
          <button 
            onClick={() => {
              setSearchTerm('');
              fetchClientes();
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
          {editingClient ? 'Editar Cliente' : 'Nuevo Cliente'}
        </h2>

        <input
          type="text"
          name="name"
          placeholder="Nombre completo"
          value={formData.name}
          onChange={handleChange}
          required
          className="w-full mb-2 p-2 border rounded"
        />

        <input
          type="email"
          name="email"
          placeholder="Correo electrónico"
          value={formData.email}
          onChange={handleChange}
          required
          className="w-full mb-2 p-2 border rounded"
        />

        <input
          type="tel"
          name="phone"
          placeholder="Teléfono"
          value={formData.phone}
          onChange={handleChange}
          className="w-full mb-4 p-2 border rounded"
        />

        <div className="flex gap-2">
          <button type="submit" className="bg-pink-600 text-white py-2 px-4 rounded hover:bg-pink-700">
            {editingClient ? 'Actualizar' : 'Crear'} Cliente
          </button>
          {editingClient && (
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

      {/* Lista de clientes */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {clientes.map(cliente => (
          <div key={cliente.id} className="border p-4 rounded shadow">
            <h3 className="text-lg font-semibold mb-2">{cliente.name}</h3>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Email:</span> {cliente.email}
            </p>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Teléfono:</span> {cliente.phone || 'No especificado'}
            </p>
            <p className="text-gray-500 text-sm mb-4">
              <span className="font-medium">Registrado:</span> {new Date(cliente.created_at).toLocaleDateString()}
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => handleEdit(cliente)}
                className="flex-1 bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
              >
                Editar
              </button>
              <button
                onClick={() => handleDelete(cliente.id)}
                className="flex-1 bg-red-600 text-white py-2 px-4 rounded hover:bg-red-700"
              >
                Eliminar
              </button>
            </div>
          </div>
        ))}
      </div>

      {clientes.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No hay clientes registrados.
        </div>
      )}
    </div>
  );
}
