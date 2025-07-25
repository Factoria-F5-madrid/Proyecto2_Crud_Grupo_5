import { useState, useEffect } from 'react';
import { productAPI, categoryAPI, handleAPIError, downloadFile } from '../services/api';

export default function PrendasCRUD() {
  const [prendas, setPrendas] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingProduct, setEditingProduct] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    category: '',
    price_min: '',
    price_max: '',
    ordering: '-created_at'
  });

  // Formulario para nueva prenda
  const [formData, setFormData] = useState({
    name: '',
    size: '',
    color: '',
    price: '',
    stock: '',
    category: '',
    description: '',
    image: null, // archivo
  });

  useEffect(() => {
    fetchPrendas();
    fetchCategories();
  }, []);

  const fetchPrendas = async () => {
    try {
      setLoading(true);
      const params = {
        ...filters,
        search: searchTerm
      }
      const response = await productAPI.getAll(params);
      setPrendas(response.data.results || response.data);
      setError(null);
    } catch (err) {
      const errorInfo = handleAPIError(err);
      setError(errorInfo.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await categoryAPI.getAll();
      setCategories(response.data.results || response.data);
    } catch (err) {
      console.error('Error al cargar categorías:', err);
    }
  };

  // Manejador cambio inputs normales
  const handleChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // Manejador cambio input file
  const handleFileChange = e => {
    setFormData(prev => ({ ...prev, image: e.target.files[0] }));
  };

  // Aplicar filtros
  const applyFilters = () => {
    fetchPrendas();
  };

  // Resetear formulario
  const resetForm = () => {
    setFormData({
      name: '',
      size: '',
      color: '',
      price: '',
      stock: '',
      category: '',
      description: '',
      image: null,
    });
    setEditingProduct(null);
  };

  // Crear o actualizar prenda
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingProduct) {
        // Actualizar
        await productAPI.partialUpdate(editingProduct.id, formData);
      } else {
        // Crear
        await productAPI.create(formData);
      }
      
      resetForm();
      fetchPrendas();
    } catch (err) {
      const errorInfo = handleAPIError(err);
      alert(errorInfo.message);
      console.error(err);
    }
  };

  // Editar prenda
  const handleEdit = (prenda) => {
    setFormData({
      name: prenda.name,
      size: prenda.size || '',
      color: prenda.color || '',
      price: prenda.price,
      stock: prenda.stock,
      category: prenda.category,
      description: prenda.description || '',
      image: null, // No pre-cargar imagen
    });
    setEditingProduct(prenda);
  };

  // Eliminar prenda
  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar esta prenda?')) {
      try {
        await productAPI.delete(id);
        fetchPrendas();
      } catch (err) {
        const errorInfo = handleAPIError(err);
        alert(errorInfo.message);
      }
    }
  };

  // Exportar CSV
  const handleExportCSV = async () => {
    try {
      const response = await productAPI.exportCSV();
      downloadFile(response.data, 'productos.csv');
    } catch (err) {
      const errorInfo = handleAPIError(err);
      alert(errorInfo.message);
    }
  };

  if (loading) return <p>Cargando prendas...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Gestión de Prendas</h1>
        <button 
          onClick={handleExportCSV}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Exportar CSV
        </button>
      </div>

      {/* Filtros y búsqueda */}
      <div className="mb-6 p-4 border rounded shadow bg-gray-50">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <input
            type="text"
            placeholder="Buscar productos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="p-2 border rounded"
          />
          <select
            value={filters.category}
            onChange={(e) => setFilters({...filters, category: e.target.value})}
            className="p-2 border rounded"
          >
            <option value="">Todas las categorías</option>
            {categories.map(cat => (
              <option key={cat.id} value={cat.id}>{cat.name}</option>
            ))}
          </select>
          <input
            type="number"
            placeholder="Precio mín"
            value={filters.price_min}
            onChange={(e) => setFilters({...filters, price_min: e.target.value})}
            className="p-2 border rounded"
          />
          <input
            type="number"
            placeholder="Precio máx"
            value={filters.price_max}
            onChange={(e) => setFilters({...filters, price_max: e.target.value})}
            className="p-2 border rounded"
          />
        </div>
        <div className="flex gap-2">
          <button 
            type="button"
            onClick={applyFilters}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Aplicar Filtros
          </button>
          <button 
            type="button"
            onClick={() => {
              setSearchTerm('');
              setFilters({category: '', price_min: '', price_max: '', ordering: '-created_at'});
              fetchPrendas();
            }}
            className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
          >
            Limpiar
          </button>
        </div>
      </div>

      {/* Formulario creación/edición */}
      <form onSubmit={handleSubmit} className="mb-8 max-w-md border p-4 rounded shadow">
        <h2 className="text-xl mb-4 font-semibold">
          {editingProduct ? 'Editar Prenda' : 'Nueva Prenda'}
        </h2>

        <input
          type="text"
          name="name"
          placeholder="Nombre"
          value={formData.name}
          onChange={handleChange}
          required
          className="w-full mb-2 p-2 border rounded"
        />

        <input
          type="text"
          name="size"
          placeholder="Talla"
          value={formData.size}
          onChange={handleChange}
          className="w-full mb-2 p-2 border rounded"
        />

        <input
          type="text"
          name="color"
          placeholder="Color"
          value={formData.color}
          onChange={handleChange}
          className="w-full mb-2 p-2 border rounded"
        />

        <input
          type="number"
          name="price"
          placeholder="Precio"
          value={formData.price}
          onChange={handleChange}
          step="0.01"
          className="w-full mb-2 p-2 border rounded"
        />

        <input
          type="number"
          name="stock"
          placeholder="Stock"
          value={formData.stock}
          onChange={handleChange}
          className="w-full mb-2 p-2 border rounded"
        />

        <select
          name="category"
          value={formData.category}
          onChange={handleChange}
          className="w-full mb-2 p-2 border rounded"
        >
          <option value="">Seleccionar categoría</option>
          {categories.map(cat => (
            <option key={cat.id} value={cat.id}>{cat.name}</option>
          ))}
        </select>

        <textarea
          name="description"
          placeholder="Descripción"
          value={formData.description}
          onChange={handleChange}
          className="w-full mb-2 p-2 border rounded"
          rows="3"
        />

        <input
          type="file"
          name="image"
          accept="image/*"
          onChange={handleFileChange}
          className="mb-4"
        />

        <div className="flex gap-2">
          <button type="submit" className="bg-pink-600 text-white py-2 px-4 rounded hover:bg-pink-700">
            {editingProduct ? 'Actualizar' : 'Crear'} Prenda
          </button>
          {editingProduct && (
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

      {/* Listado prendas */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {prendas.map(prenda => (
          <div key={prenda.id} className="border p-4 rounded shadow">
            <img
              src={prenda.image_url || 'https://via.placeholder.com/150?text=Sin+Imagen'}
              alt={prenda.name}
              className="w-full h-48 object-cover rounded mb-4"
            />
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">{prenda.name}</h3>
              <p className="text-gray-600">Talla: {prenda.size || 'N/A'}</p>
              <p className="text-gray-600">Color: {prenda.color || 'N/A'}</p>
              <p className="text-xl font-bold text-green-600">${prenda.price}</p>
              <p className="text-gray-600">Stock: {prenda.stock}</p>
              <p className="text-gray-600">Categoría: {prenda.category_name || 'Sin categoría'}</p>
              {prenda.description && (
                <p className="text-sm text-gray-500 mt-2">{prenda.description}</p>
              )}
            </div>
            <div className="flex gap-2 mt-4">
              <button
                onClick={() => handleEdit(prenda)}
                className="flex-1 bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
              >
                Editar
              </button>
              <button
                onClick={() => handleDelete(prenda.id)}
                className="flex-1 bg-red-600 text-white py-2 px-4 rounded hover:bg-red-700"
              >
                Eliminar
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
