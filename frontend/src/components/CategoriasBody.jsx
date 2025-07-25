import { useState, useEffect } from 'react';
import { categoryAPI, handleAPIError } from '../services/api';

export default function CategoriasBody() {
  const [categorias, setCategorias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingCategory, setEditingCategory] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  // Formulario para nueva categoría
  const [formData, setFormData] = useState({
    name: '',
    description: '',
  });

  useEffect(() => {
    fetchCategorias();
  }, []);

  const fetchCategorias = async () => {
    try {
      setLoading(true);
      const params = searchTerm ? { search: searchTerm } : {};
      const response = await categoryAPI.getAll(params);
      setCategorias(response.data.results || response.data);
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
    setFormData({ name: '', description: '' });
    setEditingCategory(null);
  };

  // Crear o actualizar categoría
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingCategory) {
        await categoryAPI.partialUpdate(editingCategory.id, formData);
      } else {
        await categoryAPI.create(formData);
      }
      resetForm();
      fetchCategorias();
    } catch (err) {
      const errorInfo = handleAPIError(err);
      alert(errorInfo.message);
    }
  };

  // Editar categoría
  const handleEdit = (categoria) => {
    setFormData({
      name: categoria.name,
      description: categoria.description || '',
    });
    setEditingCategory(categoria);
  };

  // Eliminar categoría
  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar esta categoría?')) {
      try {
        await categoryAPI.delete(id);
        fetchCategorias();
      } catch (err) {
        const errorInfo = handleAPIError(err);
        alert(errorInfo.message);
      }
    }
  };

  if (loading) return <p className="p-6">Cargando categorías...</p>;
  if (error) return <p className="p-6 text-red-600">{error}</p>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Gestión de Categorías</h1>
      </div>

      {/* Búsqueda */}
      <div className="mb-6 p-4 border rounded shadow bg-gray-50">
        <div className="flex gap-4">
          <input
            type="text"
            placeholder="Buscar categorías por nombre..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 p-2 border rounded"
          />
          <button 
            onClick={fetchCategorias}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Buscar
          </button>
          <button 
            onClick={() => {
              setSearchTerm('');
              fetchCategorias();
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
          {editingCategory ? 'Editar Categoría' : 'Nueva Categoría'}
        </h2>

        <input
          type="text"
          name="name"
          placeholder="Nombre de la categoría"
          value={formData.name}
          onChange={handleChange}
          required
          className="w-full mb-2 p-2 border rounded"
        />

        <textarea
          name="description"
          placeholder="Descripción (opcional)"
          value={formData.description}
          onChange={handleChange}
          className="w-full mb-4 p-2 border rounded"
          rows="3"
        />

        <div className="flex gap-2">
          <button type="submit" className="bg-pink-600 text-white py-2 px-4 rounded hover:bg-pink-700">
            {editingCategory ? 'Actualizar' : 'Crear'} Categoría
          </button>
          {editingCategory && (
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

      {/* Lista de categorías */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {categorias.map(categoria => (
          <div key={categoria.id} className="border p-4 rounded shadow">
            <h3 className="text-lg font-semibold mb-2">{categoria.name}</h3>
            <p className="text-gray-600 mb-4">
              {categoria.description || 'Sin descripción'}
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => handleEdit(categoria)}
                className="flex-1 bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
              >
                Editar
              </button>
              <button
                onClick={() => handleDelete(categoria.id)}
                className="flex-1 bg-red-600 text-white py-2 px-4 rounded hover:bg-red-700"
              >
                Eliminar
              </button>
            </div>
          </div>
        ))}
      </div>

      {categorias.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No hay categorías registradas.
        </div>
      )}
    </div>
  );
}
