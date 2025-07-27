import { useState, useEffect } from "react";
import { FiEdit2, FiTrash2, FiPlus, FiCheck, FiX } from "react-icons/fi";
import { customerAPI, handleAPIError } from '../services/api';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const ClientesBody = () => {
  const [data, setData] = useState([]);

  const [columns, setColumns] = useState([
    { key: "name", label: "Nombre", editable: true },
    { key: "email", label: "Email", editable: true },
    { key: "phone", label: "Teléfono", editable: true },
    { key: "created_at", label: "Fecha de Creación", editable: false }
  ]);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      const response = await customerAPI.getAll();
      setData(response.data.results || response.data);
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(`Error al cargar clientes: ${errorInfo.message}`);
    }
  };

  const [editingItem, setEditingItem] = useState(null);
  const [newItem, setNewItem] = useState({});
  const [isAdding, setIsAdding] = useState(false);
  const [newColumn, setNewColumn] = useState({ key: "", label: "", editable: true });

  const handleEdit = (item) => {
    setEditingItem({ ...item });
  };

  const handleUpdate = async () => {
    try {
      await customerAPI.update(editingItem.id, editingItem);
      toast.success("Cliente actualizado exitosamente");
      setEditingItem(null);
      await fetchCustomers();
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(`Error al actualizar cliente: ${errorInfo.message}`);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("¿Estás seguro de que quieres eliminar este cliente?")) {
      try {
        await customerAPI.delete(id);
        toast.success("Cliente eliminado exitosamente");
        await fetchCustomers();
      } catch (error) {
        const errorInfo = handleAPIError(error);
        toast.error(`Error al eliminar cliente: ${errorInfo.message}`);
      }
    }
  };

  const handleAdd = async () => {
    try {
      await customerAPI.create(newItem);
      toast.success("Cliente añadido exitosamente");
      setIsAdding(false);
      setNewItem({});
      await fetchCustomers();
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(`Error al añadir cliente: ${errorInfo.message}`);
    }
  };

  const handleAddColumn = () => {
    if (newColumn.key && newColumn.label) {
      setColumns([...columns, newColumn]);
      setNewColumn({ key: "", label: "", editable: true });
    }
  };

  const handleRemoveColumn = (key) => {
    setColumns(columns.filter((col) => col.key !== key));
  };

  return (
    <div className="p-6 max-w-6xl mx-auto bg-white rounded-lg shadow-lg">
      <div className="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h2 className="text-2xl font-bold text-gray-800">Clientes</h2>
        <button
          onClick={() => setIsAdding(true)}
          className="flex items-center gap-2 px-4 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600 transition-colors"
          aria-label="Agregar nuevo cliente"
        >
          <FiPlus /> Agregar Nuevo
        </button>
      </div>

      <div className="mb-6 p-4 border rounded-md bg-gray-50">
        <h3 className="text-lg font-semibold mb-4">Gestionar Columnas</h3>
        <div className="flex flex-wrap gap-4">
          {columns.map((col) => (
            <div key={col.key} className="flex items-center gap-2 bg-white p-2 rounded-md shadow-sm">
              <span>{col.label}</span>
              <button
                onClick={() => handleRemoveColumn(col.key)}
                className="text-red-500 hover:text-red-700"
                aria-label={`Eliminar columna ${col.label}`}
              >
                <FiX />
              </button>
            </div>
          ))}
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Clave"
              className="px-3 py-1 border rounded-md"
              value={newColumn.key}
              onChange={(e) => setNewColumn({ ...newColumn, key: e.target.value })}
            />
            <input
              type="text"
              placeholder="Etiqueta"
              className="px-3 py-1 border rounded-md"
              value={newColumn.label}
              onChange={(e) => setNewColumn({ ...newColumn, label: e.target.value })}
            />
            <button
              onClick={handleAddColumn}
              className="px-3 py-1 bg-orange-500 text-white rounded-md hover:bg-orange-600"
              aria-label="Agregar nueva columna"
            >
              Agregar
            </button>
          </div>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse" role="grid">
          <thead>
            <tr className="bg-gray-100">
              {columns.map((col) => (
                <th key={col.key} className="p-3 text-left font-semibold text-gray-600">
                  {col.label}
                </th>
              ))}
              <th className="p-3 text-left font-semibold text-gray-600">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item) => (
              <tr
                key={item.id}
                className="border-t hover:bg-gray-50 transition-colors"
                role="row"
              >
                {columns.map((col) => (
                  <td key={`${item.id}-${col.key}`} className="p-3">
                    {editingItem?.id === item.id && col.editable ? (
                      <input
                        type="text"
                        className="w-full px-2 py-1 border rounded"
                        value={editingItem[col.key] || ""}
                        onChange={(e) =>
                          setEditingItem({ ...editingItem, [col.key]: e.target.value })
                        }
                      />
                    ) : (
                      item[col.key]
                    )}
                  </td>
                ))}
                <td className="p-3">
                  <div className="flex gap-2">
                    {editingItem?.id === item.id ? (
                      <>
                        <button
                          onClick={handleUpdate}
                          className="p-2 text-green-500 hover:text-green-600"
                          aria-label="Guardar cambios"
                        >
                          <FiCheck />
                        </button>
                        <button
                          onClick={() => setEditingItem(null)}
                          className="p-2 text-gray-500 hover:text-gray-700"
                          aria-label="Cancelar edición"
                        >
                          <FiX />
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          onClick={() => handleEdit(item)}
                          className="p-2 text-orange-500 hover:text-orange-600"
                          aria-label="Editar cliente"
                        >
                          <FiEdit2 />
                        </button>
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="p-2 text-red-500 hover:text-red-700"
                          aria-label="Eliminar cliente"
                        >
                          <FiTrash2 />
                        </button>
                      </>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {isAdding && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h3 className="text-xl font-semibold mb-4">Agregar Nuevo Cliente</h3>
            {columns.filter(col => col.editable).map((col) => (
              <div key={col.key} className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">{col.label}</label>
                <input
                  type="text"
                  className="w-full px-3 py-2 border rounded-md"
                  value={newItem[col.key] || ""}
                  onChange={(e) => setNewItem({ ...newItem, [col.key]: e.target.value })}
                />
              </div>
            ))}
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setIsAdding(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                Cancelar
              </button>
              <button
                onClick={handleAdd}
                className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600"
              >
                Agregar
              </button>
            </div>
          </div>
        </div>
      )}
      <ToastContainer position="bottom-right" />
    </div>
  );
};

export default ClientesBody;
