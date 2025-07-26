import { useState, useEffect } from 'react';
import { orderAPI, handleAPIError, downloadFile } from '../services/api';

export default function VentasBody() {
  const [ventas, setVentas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchVentas();
  }, []);

  const fetchVentas = async () => {
    try {
      setLoading(true);
      const response = await orderAPI.getAll();
      setVentas(response.data.results || response.data);
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

      {/* Lista de ventas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {ventas.map((venta) => (
          <div key={venta.id} className="border p-4 rounded shadow">
            <h3 className="text-lg font-semibold mb-2">Venta ID: {venta.id}</h3>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Cliente:</span> {venta.customer.name}  
            </p>
            <p className="text-gray-600 mb-1">
              <span className="font-medium">Total:</span> ${venta.total}
            </p>
            <p className="text-gray-500 text-sm mb-4">
              <span className="font-medium">Fecha:</span> {new Date(venta.date).toLocaleDateString()}
            </p>
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
