import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from '@/pages/Dashboard.jsx';
import Prendas from '@/pages/Prendas';
import Clientes from '@/pages/Clientes';
import Usuarias from '@/pages/Usuarias';
import Categorias from '@/pages/Categorias';
import Ventas from '@/pages/Ventas';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/prendas" element={<Prendas />} />
        <Route path="/clientes" element={<Clientes />} />
        <Route path="/usuarias" element={<Usuarias />} />
        <Route path="/categorias" element={<Categorias />} />
        <Route path="/ventas" element={<Ventas />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;