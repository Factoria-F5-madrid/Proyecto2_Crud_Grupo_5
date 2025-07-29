import React, { useState, useEffect } from "react";
import { FiEdit2, FiTrash2, FiPlus, FiX, FiCheck, FiFilter, FiSearch } from "react-icons/fi";
import { BsArrowUp, BsArrowDown } from "react-icons/bs";
import { productAPI, categoryAPI, handleAPIError } from '../services/api';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const CRUDApplication = () => {
  const [items, setItems] = useState([]);

  const [formData, setFormData] = useState({
    name: "",
    category: "",
    price: "",
    stock: "",
    size: "",
    color: "",
    description: "",
    image: null
  });
  
  const [categories, setCategories] = useState([]);
  
  // Categorías estáticas para el formulario y filtros
  const staticCategories = [
    { id: 'camisetas', name: 'Camisetas' },
    { id: 'pantalon', name: 'Pantalón' },
    { id: 'hombre', name: 'Hombre' },
    { id: 'mujer', name: 'Mujer' },
    { id: 'nino', name: 'Niño' },
    { id: 'verano', name: 'Verano' },
    { id: 'invierno', name: 'Invierno' }
  ];

  const [isEditing, setIsEditing] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleteId, setDeleteId] = useState(null);
  const [sortField, setSortField] = useState(null);
  const [sortDirection, setSortDirection] = useState("asc");
  const [filterCategory, setFilterCategory] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Cargar datos al montar el componente
  useEffect(() => {
    fetchProducts();
    // Cargar categorías estáticas
    setCategories(staticCategories);
  }, []);

  const fetchProducts = async () => {
    try {
      setIsLoading(true);
      const response = await productAPI.getAll();
      setItems(response.data.results || response.data);
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(`Error al cargar productos: ${errorInfo.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await categoryAPI.getAll();
      setCategories(response.data.results || response.data);
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(`Error al cargar categorías: ${errorInfo.message}`);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, files } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === "file" ? files[0] : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      if (isEditing) {
        const response = await productAPI.update(editingId, formData);
        toast.success('Producto actualizado exitosamente');
        setIsEditing(false);
        setEditingId(null);
      } else {
        const response = await productAPI.create(formData);
        toast.success('Producto creado exitosamente');
      }
      
      // Resetear formulario
      setFormData({
        name: "",
        category: "",
        price: "",
        stock: "",
        size: "",
        color: "",
        description: "",
        image: null
      });
      
      // Recargar productos
      await fetchProducts();
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(`Error al ${isEditing ? 'actualizar' : 'crear'} producto: ${errorInfo.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = (item) => {
    setFormData(item);
    setIsEditing(true);
    setEditingId(item.id);
  };

  const handleDelete = (id) => {
    setDeleteId(id);
    setShowDeleteModal(true);
  };

  const confirmDelete = async () => {
    try {
      await productAPI.delete(deleteId);
      toast.success('Producto eliminado exitosamente');
      setShowDeleteModal(false);
      setDeleteId(null);
      await fetchProducts();
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(`Error al eliminar producto: ${errorInfo.message}`);
    }
  };

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(prev => prev === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  const filteredAndSortedItems = items
    .filter(item => {
      const matchesCategory = !filterCategory || item.category === filterCategory;
      const matchesSearch = !searchQuery || 
        item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.category.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesCategory && matchesSearch;
    })
    .sort((a, b) => {
      if (!sortField) return 0;
      const aValue = a[sortField];
      const bValue = b[sortField];
      return sortDirection === "asc" ? 
        (aValue > bValue ? 1 : -1) :
        (aValue < bValue ? 1 : -1);
    });

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-7xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-2xl font-bold mb-4">{isEditing ? "Edit Item" : "Create New Item"}</h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700">Name</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-orange-500 focus:ring-orange-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="category" className="block text-sm font-medium text-gray-700">Categoría</label>
                <select
                  id="category"
                  name="category"
                  value={formData.category}
                  onChange={handleInputChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  required
                >
                  <option value="">Seleccionar Categoría</option>
                  {staticCategories.map(category => (
                    <option key={category.id} value={category.id}>{category.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="price" className="block text-sm font-medium text-gray-700">Precio</label>
                <input
                  type="number"
                  step="0.01"
                  id="price"
                  name="price"
                  value={formData.price}
                  onChange={handleInputChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="stock" className="block text-sm font-medium text-gray-700">Stock</label>
                <input
                  type="number"
                  id="stock"
                  name="stock"
                  value={formData.stock}
                  onChange={handleInputChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="size" className="block text-sm font-medium text-gray-700">Talla</label>
                <input
                  type="text"
                  id="size"
                  name="size"
                  value={formData.size}
                  onChange={handleInputChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label htmlFor="color" className="block text-sm font-medium text-gray-700">Color</label>
                <input
                  type="text"
                  id="color"
                  name="color"
                  value={formData.color}
                  onChange={handleInputChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>

              <div className="col-span-2">
                <label htmlFor="description" className="block text-sm font-medium text-gray-700">Descripción</label>
                <textarea
                  id="description"
                  name="description"
                  rows="3"
                  value={formData.description}
                  onChange={handleInputChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  placeholder="Descripción del producto..."
                />
              </div>

              <div className="col-span-2">
                <label htmlFor="image" className="block text-sm font-medium text-gray-700">Imagen</label>
                <input
                  type="file"
                  id="image"
                  name="image"
                  onChange={handleInputChange}
                  className="mt-1 block w-full text-sm text-gray-500
                    file:mr-4 file:py-2 file:px-4
                    file:rounded-full file:border-0
                    file:text-sm file:font-semibold
                    file:bg-indigo-50 file:text-orange-700
                    hover:file:bg-indigo-100"
                  accept="image/*"
                />
              </div>
            </div>

            <div className="flex justify-end space-x-3">
              {isEditing && (
                <button
                  type="button"
                  onClick={() => {
                    setIsEditing(false);
                    setEditingId(null);
                    setFormData({
                      name: "",
                      category: "",
                      price: "",
                      stock: "",
                      size: "",
                      color: "",
                      description: "",
                      image: null
                    });
                  }}
                  className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500"
                >
                  Cancel
                </button>
              )}
              <button
                type="submit"
                disabled={isLoading}
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-orange-600 hover:bg-orange-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500"
              >
                {isLoading ? (
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                ) : null}
                {isEditing ? "Update" : "Create"} Item
              </button>
            </div>
          </form>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex flex-col sm:flex-row justify-between items-center mb-4 space-y-3 sm:space-y-0">
            <h2 className="text-2xl font-bold">Items List</h2>
            
            <div className="flex space-x-4">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search items..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
                <FiSearch className="absolute left-3 top-3 text-gray-400" />
              </div>

              <select
                value={filterCategory}
                onChange={(e) => setFilterCategory(e.target.value)}
                className="border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500"
              >
                <option value="">Todas las Categorías</option>
                {staticCategories.map(category => (
                  <option key={category.id} value={category.id}>{category.name}</option>
                ))}
              </select>
            </div>
          </div>

          {isLoading ? (
            <div className="flex justify-center items-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredAndSortedItems.map((item) => {
                // Buscar primero en categorías estáticas, luego en categorías de la API
                const categoryName = staticCategories.find(cat => cat.id === item.category)?.name || 
                                   categories.find(cat => cat.id === item.category)?.name || 
                                   'Sin categoría';
                const imageUrl = item.image ? (item.image.startsWith('http') ? item.image : `http://localhost:8000${item.image}`) : "https://images.unsplash.com/photo-1560393464-5c69a73c5770";
                
                return (
                  <div key={item.id} className="bg-white border rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-300">
                    <img
                      src={imageUrl}
                      alt={item.name}
                      className="w-full h-48 object-cover"
                      onError={(e) => {
                        e.target.src = "https://images.unsplash.com/photo-1560393464-5c69a73c5770";
                      }}
                    />
                    <div className="p-4">
                      <h3 className="text-lg font-semibold mb-2">{item.name}</h3>
                      <p className="text-gray-600 mb-1">Categoría: {categoryName}</p>
                      <p className="text-gray-600 mb-1">Precio: ${item.price}</p>
                      <p className="text-gray-600 mb-1">Stock: {item.stock}</p>
                      {item.size && <p className="text-gray-600 mb-1">Talla: {item.size}</p>}
                      {item.color && <p className="text-gray-600 mb-1">Color: {item.color}</p>}
                      {item.description && <p className="text-gray-500 text-sm mb-2">{item.description}</p>}
                      <p className="mb-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${item.stock > 0 ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}`}>
                          {item.stock > 0 ? "En Stock" : "Sin Stock"}
                        </span>
                      </p>
                      <div className="flex justify-end space-x-2">
                        <button
                          onClick={() => handleEdit(item)}
                          className="p-2 text-orange-600 hover:bg-blue-50 rounded-full"
                          aria-label="Edit item"
                        >
                          <FiEdit2 className="w-5 h-5" />
                        </button>
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="p-2 text-red-600 hover:bg-red-50 rounded-full"
                          aria-label="Delete item"
                        >
                          <FiTrash2 className="w-5 h-5" />
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-medium mb-4">Confirm Deletion</h3>
            <p className="text-gray-500 mb-6">Are you sure you want to delete this item? This action cannot be undone.</p>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setShowDeleteModal(false)}
                className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500"
              >
                Cancel
              </button>
              <button
                onClick={confirmDelete}
                className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
      <ToastContainer position="bottom-right" />
    </div>
  );
};

export default CRUDApplication;
