import axios from 'axios';
import { useState, useEffect } from 'react';

export default function PrendasList() {
  const [prendas, setPrendas] = useState([]);

  useEffect(() => {
    axios
      .get('http://localhost:8000/api/prenda/')
      .then(response => setPrendas(response.data))
      .catch(error => console.error('Error al cargar prendas:', error));
  }, []);

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      {prendas.map(prenda => (
        <div key={prenda.id} className="p-4 border rounded shadow">
          <h3 className="font-semibold text-lg">{prenda.name}</h3>
          <p className="text-gray-600">${prenda.price}</p>
        </div>
      ))}
    </div>
  );
}
