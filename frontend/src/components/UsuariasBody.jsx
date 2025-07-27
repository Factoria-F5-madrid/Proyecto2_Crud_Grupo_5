import { useState, useEffect } from "react";
import { FaEdit, FaTrash, FaPlus } from "react-icons/fa";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { usuariaAPI, handleAPIError } from '../services/api';

const CRUDTable = () => {
  const [data, setData] = useState([]);

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    first_name: "",
    last_name: "",
    phone: "",
    role: "EMPLOYEE",
    status: "ACTIVE",
    hire_date: "",
    salary: "",
    address: "",
    avatar: null,
    password: "",
    password_confirm: ""
  });

  useEffect(() => {
    fetchUsuarias();
  }, []);

  const fetchUsuarias = async () => {
    try {
      const response = await usuariaAPI.getAll();
      setData(response.data.results || response.data);
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(`Error al cargar usuarias: ${errorInfo.message}`);
    }
  };

  const [editingId, setEditingId] = useState(null);
  const [isFormVisible, setIsFormVisible] = useState(false);

  const handleInputChange = (e) => {
    const { name, value, type, files } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "file" ? files[0] : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await usuariaAPI.update(editingId, formData);
        toast.success("Usuaria actualizada exitosamente!");
      } else {
        await usuariaAPI.create(formData);
        toast.success("Usuaria creada exitosamente!");
      }
      resetForm();
      await fetchUsuarias();
    } catch (error) {
      const errorInfo = handleAPIError(error);
      toast.error(`Error al ${editingId ? 'actualizar' : 'crear'} usuaria: ${errorInfo.message}`);
    }
  };

  const handleEdit = (item) => {
    setFormData({
      username: item.username,
      email: item.email,
      first_name: item.first_name,
      last_name: item.last_name,
      phone: item.phone || "",
      role: item.role,
      status: item.status,
      hire_date: item.hire_date || "",
      salary: item.salary || "",
      address: item.address || "",
      avatar: null,
      password: "",
      password_confirm: ""
    });
    setEditingId(item.id);
    setIsFormVisible(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm("¿Estás seguro de que quieres eliminar esta usuaria?")) {
      try {
        await usuariaAPI.delete(id);
        // Actualizar la lista local inmediatamente para mejor UX
        setData(prevData => prevData.filter(item => item.id !== id));
        toast.success("Usuaria eliminada exitosamente!");
      } catch (error) {
        const errorInfo = handleAPIError(error);
        toast.error(`Error al eliminar usuaria: ${errorInfo.message}`);
        // Si hay error, recargar la lista para mantener consistencia
        await fetchUsuarias();
      }
    }
  };

  const resetForm = () => {
    setFormData({
      username: "",
      email: "",
      first_name: "",
      last_name: "",
      phone: "",
      role: "EMPLOYEE",
      status: "ACTIVE",
      hire_date: "",
      salary: "",
      address: "",
      avatar: null,
      password: "",
      password_confirm: ""
    });
    setEditingId(null);
    setIsFormVisible(false);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Usuarias</h1>
        <button
          onClick={() => setIsFormVisible(!isFormVisible)}
          className="bg-[#F28D35] hover:bg-[#3D2C4E] text-white px-4 py-2 rounded-lg flex items-center gap-2 transition duration-300"
        >
          <FaPlus /> {isFormVisible ? "Hide Form" : "Add New"}
        </button>
      </div>

      {isFormVisible && (
        <form
          onSubmit={handleSubmit}
          className="bg-white p-6 rounded-lg shadow-md mb-6"
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-gray-700 mb-2">Username</label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-gray-700 mb-2">First Name</label>
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-gray-700 mb-2">Last Name</label>
              <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-gray-700 mb-2">Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-gray-700 mb-2">Phone</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-gray-700 mb-2">Role</label>
              <select
                name="role"
                value={formData.role}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="EMPLOYEE">Empleada</option>
                <option value="ADMIN">Administradora</option>
                <option value="MANAGER">Gerente</option>
              </select>
            </div>
            <div>
              <label className="block text-gray-700 mb-2">Status</label>
              <select
                name="status"
                value={formData.status}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="ACTIVE">Activa</option>
                <option value="INACTIVE">Inactiva</option>
                <option value="SUSPENDED">Suspendida</option>
              </select>
            </div>
            <div>
              <label className="block text-gray-700 mb-2">Hire Date</label>
              <input
                type="date"
                name="hire_date"
                value={formData.hire_date}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-gray-700 mb-2">Salary</label>
              <input
                type="number"
                step="0.01"
                name="salary"
                value={formData.salary}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="md:col-span-3">
              <label className="block text-gray-700 mb-2">Address</label>
              <textarea
                name="address"
                value={formData.address}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows="2"
              />
            </div>
            <div className="md:col-span-3">
              <label className="block text-gray-700 mb-2">Avatar</label>
              <input
                type="file"
                name="avatar"
                onChange={handleInputChange}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                accept="image/*"
              />
            </div>
          </div>
          <div className="mt-4 flex justify-end gap-2">
            <button
              type="button"
              onClick={resetForm}
              className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg transition duration-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition duration-300"
            >
              {editingId ? "Update" : "Submit"}
            </button>
          </div>
        </form>
      )}

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Avatar
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Username
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Full Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Email
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Role
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {data.map((item) => {
                const avatarUrl = item.avatar ? (item.avatar.startsWith('http') ? item.avatar : `http://localhost:8000${item.avatar}`) : "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e";
                return (
                <tr key={item.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {item.id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <img 
                      src={avatarUrl} 
                      alt={item.username}
                      className="h-10 w-10 rounded-full object-cover"
                      onError={(e) => {
                        e.target.src = "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e";
                      }}
                    />
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {item.username}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {item.first_name} {item.last_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {item.email}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      item.role === 'ADMIN' ? 'bg-purple-100 text-purple-800' :
                      item.role === 'MANAGER' ? 'bg-blue-100 text-blue-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {item.role === 'ADMIN' ? 'Administradora' :
                       item.role === 'MANAGER' ? 'Gerente' : 'Empleada'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      item.status === 'ACTIVE' ? 'bg-green-100 text-green-800' :
                      item.status === 'SUSPENDED' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {item.status === 'ACTIVE' ? 'Activa' :
                       item.status === 'SUSPENDED' ? 'Suspendida' : 'Inactiva'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button
                      onClick={() => handleEdit(item)}
                      className="text-orange-500 hover:text-orange-600 mr-4"
                      aria-label="Edit entry"
                    >
                      <FaEdit className="text-xl" />
                    </button>
                    <button
                      onClick={() => handleDelete(item.id)}
                      className="text-red-600 hover:text-red-900"
                      aria-label="Delete entry"
                    >
                      <FaTrash className="text-xl" />
                    </button>
                  </td>
                </tr>
                );
              })} 
            </tbody>
          </table>
        </div>
      </div>
      <ToastContainer position="bottom-right" />
    </div>
  );
};

export default CRUDTable;