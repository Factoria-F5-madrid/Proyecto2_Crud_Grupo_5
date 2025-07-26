import { useState, useEffect } from 'react';
import { usuariaAPI, handleAPIError, downloadFile } from '../services/api';

export default function UsuariasBody() {
  const [usuarias, setUsuarias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingUsuaria, setEditingUsuaria] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  // Formulario para nueva usuaria
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    phone: '',
    role: 'EMPLOYEE',
    status: 'ACTIVE',
    avatar: null,
    hire_date: '',
    salary: '',
    address: '',
    password: '',
    password_confirm: '',
  });

  useEffect(() => {
    fetchUsuarias();
  }, []);

  const fetchUsuarias = async () => {
    try {
      setLoading(true);
      const params = searchTerm ? { search: searchTerm } : {};
      const response = await usuariaAPI.getAll(params);
      setUsuarias(response.data.results || response.data);
      setError(null);
    } catch (err) {
      const errorInfo = handleAPIError(err);
      setError(errorInfo.message);
    } finally {
      setLoading(false);
    }
  };

  // Manejador cambio inputs
  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === 'avatar') {
      setFormData(prev => ({ ...prev, [name]: files[0] || null }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  // Resetear formulario
  const resetForm = () => {
    setFormData({
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      phone: '',
      role: 'EMPLOYEE',
      status: 'ACTIVE',
      avatar: null,
      hire_date: '',
      salary: '',
      address: '',
      password: '',
      password_confirm: '',
    });
    setEditingUsuaria(null);
    // Limpiar el input de archivo
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) fileInput.value = '';
  };

  // Crear o actualizar usuaria
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Log de debug para ver qué datos se están enviando
    console.log('Datos del formulario a enviar:', formData);
    
    try {
      if (editingUsuaria) {
        await usuariaAPI.partialUpdate(editingUsuaria.id, formData);
      } else {
        await usuariaAPI.create(formData);
      }
      resetForm();
      fetchUsuarias();
    } catch (err) {
      // Log detallado del error
      console.error('Error completo:', err);
      console.error('Response data:', err.response?.data);
      console.error('Response status:', err.response?.status);
      
      const errorInfo = handleAPIError(err);
      
      // Mostrar más detalles del error
      let errorMessage = errorInfo.message;
      if (err.response?.data) {
        errorMessage += '\nDetalles: ' + JSON.stringify(err.response.data, null, 2);
      }
      
      alert(errorMessage);
    }
  };

  // Editar usuaria
  const handleEdit = (usuaria) => {
    setFormData({
      username: usuaria.username,
      email: usuaria.email,
      first_name: usuaria.first_name,
      last_name: usuaria.last_name,
      phone: usuaria.phone || '',
      role: usuaria.role,
      status: usuaria.status,
      avatar: null, // No pre-cargar foto existente
      hire_date: usuaria.hire_date || '',
      salary: usuaria.salary || '',
      address: usuaria.address || '',
      password: '', // No pre-cargar contraseña
      password_confirm: '', // No pre-cargar confirmación
    });
    setEditingUsuaria(usuaria);
  };

  // Eliminar usuaria
  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar esta usuaria?')) {
      try {
        await usuariaAPI.delete(id);
        fetchUsuarias();
      } catch (err) {
        const errorInfo = handleAPIError(err);
        alert(errorInfo.message);
      }
    }
  };

  // Reactivar usuaria (si estaba desactivada)
  const handleReactivate = async (id) => {
    try {
      await usuariaAPI.reactivate(id);
      fetchUsuarias();
    } catch (err) {
      const errorInfo = handleAPIError(err);
      alert(errorInfo.message);
    }
  };

  const handleExportCSV = async () => {
    try {
      const response = await usuariaAPI.exportCSV();
      downloadFile(response.data, 'usuarias.csv');
    } catch (err) {
      const errorInfo = handleAPIError(err);
      alert(errorInfo.message);
    }
  };

  if (loading) return <p className="p-6">Cargando usuarias...</p>;
  if (error) return <p className="p-6 text-red-600">{error}</p>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Gestión de Usuarias</h1>
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
            placeholder="Buscar usuarias por nombre o email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 p-2 border rounded"
          />
          <button 
            onClick={fetchUsuarias}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Buscar
          </button>
          <button 
            onClick={() => {
              setSearchTerm('');
              fetchUsuarias();
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
          {editingUsuaria ? 'Editar Usuaria' : 'Nueva Usuaria'}
        </h2>

        <input
          type="text"
          name="username"
          placeholder="Nombre de usuario"
          value={formData.username}
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
          type="text"
          name="first_name"
          placeholder="Nombre"
          value={formData.first_name}
          onChange={handleChange}
          required
          className="w-full mb-2 p-2 border rounded"
        />

        <input
          type="text"
          name="last_name"
          placeholder="Apellido"
          value={formData.last_name}
          onChange={handleChange}
          required
          className="w-full mb-2 p-2 border rounded"
        />

        <input
          type="tel"
          name="phone"
          placeholder="Teléfono (+999999999)"
          value={formData.phone}
          onChange={handleChange}
          className="w-full mb-2 p-2 border rounded"
        />

        <select
          name="role"
          value={formData.role}
          onChange={handleChange}
          required
          className="w-full mb-2 p-2 border rounded"
        >
          <option value="EMPLOYEE">Empleada</option>
          <option value="ADMIN">Administradora</option>
          <option value="MANAGER">Gerente</option>
        </select>

        <select
          name="status"
          value={formData.status}
          onChange={handleChange}
          required
          className="w-full mb-2 p-2 border rounded"
        >
          <option value="ACTIVE">Activa</option>
          <option value="INACTIVE">Inactiva</option>
          <option value="SUSPENDED">Suspendida</option>
        </select>

        <input
          type="date"
          name="hire_date"
          placeholder="Fecha de contratación"
          value={formData.hire_date}
          onChange={handleChange}
          className="w-full mb-2 p-2 border rounded"
        />

        <input
          type="number"
          name="salary"
          placeholder="Salario"
          value={formData.salary}
          onChange={handleChange}
          min="0"
          step="0.01"
          className="w-full mb-2 p-2 border rounded"
        />

        <textarea
          name="address"
          placeholder="Dirección"
          value={formData.address}
          onChange={handleChange}
          rows="2"
          className="w-full mb-2 p-2 border rounded"
        ></textarea>

        <input
          type="file"
          name="avatar"
          accept="image/*"
          onChange={handleChange}
          className="w-full mb-2 p-2 border rounded"
        />
        {formData.avatar && (
          <p className="text-sm text-gray-600 mb-2">Archivo seleccionado: {formData.avatar.name}</p>
        )}

        {!editingUsuaria && (
          <>
            <input
              type="password"
              name="password"
              placeholder="Contraseña (mínimo 8 caracteres)"
              value={formData.password}
              onChange={handleChange}
              required
              minLength="8"
              className="w-full mb-2 p-2 border rounded"
            />

            <input
              type="password"
              name="password_confirm"
              placeholder="Confirmar contraseña"
              value={formData.password_confirm}
              onChange={handleChange}
              required
              minLength="8"
              className="w-full mb-4 p-2 border rounded"
            />
          </>
        )}

        <div className="flex gap-2">
          <button type="submit" className="bg-pink-600 text-white py-2 px-4 rounded hover:bg-pink-700">
            {editingUsuaria ? 'Actualizar' : 'Crear'} Usuaria
          </button>
          {editingUsuaria && (
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

      {/* Lista de usuarias */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {usuarias.map((usuaria) => (
          <div key={usuaria.id} className="border p-4 rounded shadow">
            {usuaria.avatar_url && (
              <img 
                src={usuaria.avatar_url} 
                alt={usuaria.full_name || `${usuaria.first_name} ${usuaria.last_name}`}
                className="w-16 h-16 rounded-full mx-auto mb-2 object-cover"
              />
            )}
            <h3 className="text-lg font-semibold mb-2 text-center">
              {usuaria.full_name || `${usuaria.first_name} ${usuaria.last_name}`}
            </h3>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Usuario:</span> {usuaria.username}
            </p>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Email:</span> {usuaria.email}
            </p>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Teléfono:</span> {usuaria.phone || 'No especificado'}
            </p>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Rol:</span> {usuaria.role_display || usuaria.role}
            </p>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Estado:</span> {usuaria.status}
            </p>
            {usuaria.hire_date && (
              <p className="text-gray-600 mb-1">
                <span className="font-medium">Contratación:</span> {new Date(usuaria.hire_date).toLocaleDateString()}
              </p>
            )}
            {usuaria.address && (
              <p className="text-gray-600 mb-1">
                <span className="font-medium">Dirección:</span> {usuaria.address}
              </p>
            )}
            <p className="text-gray-500 text-sm mb-4">
              <span className="font-medium">Registrada:</span> {new Date(usuaria.created_at).toLocaleDateString()}
            </p>
            
            <div className="flex gap-2">
              <button
                onClick={() => handleEdit(usuaria)}
                className="flex-1 bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
              >
                Editar
              </button>
              <button
                onClick={() => handleDelete(usuaria.id)}
                className="flex-1 bg-red-600 text-white py-2 px-4 rounded hover:bg-red-700"
              >
                Eliminar
              </button>
            </div>
            
            {usuaria.is_active === false && (
              <button
                onClick={() => handleReactivate(usuaria.id)}
                className="w-full mt-2 bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700"
              >
                Reactivar
              </button>
            )}
          </div>
        ))}
      </div>

      {usuarias.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No hay usuarias registradas.
        </div>
      )}
    </div>
  );
}
