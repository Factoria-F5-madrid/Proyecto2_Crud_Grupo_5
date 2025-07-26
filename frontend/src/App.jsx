import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from '@/pages/Dashboard.jsx';
import Prendas from '@/pages/Prendas.jsx';
import Clientes from '@/pages/Clientes.jsx';
import Usuarias from '@/pages/Usuarias.jsx';
import Ventas from '@/pages/Ventas.jsx';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/prendas" element={<Prendas />} />
        <Route path="/clientes" element={<Clientes />} />
        <Route path="/usuarias" element={<Usuarias />} />
        <Route path="/ventas" element={<Ventas />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;