import { useState, useEffect } from 'react';
import { usuariaAPI, handleAPIError, downloadFile } from '../services/api';

export default function UsuariasBody() {
  const [usuarias, setUsuarias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUsuarias();
  }, []);

  const fetchUsuarias = async () => {
    try {
      setLoading(true);
      const response = await usuariaAPI.getAll();
      setUsuarias(response.data.results || response.data);
      setError(null);
    } catch (err) {
      const errorInfo = handleAPIError(err);
      setError(errorInfo.message);
    } finally {
      setLoading(false);
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

      {/* Lista de usuarias */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {usuarias.map((usuaria) => (
          <div key={usuaria.id} className="border p-4 rounded shadow">
            <h3 className="text-lg font-semibold mb-2">{usuaria.name}</h3>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Email:</span> {usuaria.email}
            </p>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Teléfono:</span> {usuaria.phone || 'No especificado'}
            </p>
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
