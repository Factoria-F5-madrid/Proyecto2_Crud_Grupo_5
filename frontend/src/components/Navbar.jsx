import logoCirculo from '@/assets/fenix_logo_2.png';
import logoTexto from '@/assets/FENIXW.png';
import hoja1 from '@/assets/hoja_1.png';
import hoja2 from '@/assets/hoja_2.png';
import hoja3 from '@/assets/hoja_3.png';
import hoja4 from '@/assets/hoja_4.png';
import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <header className="bg-[#c85a8a] px-8 py-2">
      <div className="flex items-center gap-2 sm:gap-3">
        <img src={logoCirculo} alt="Logo Fenix" className="h-20 sm:h-22" />
        <img src={logoTexto} alt="FENIX" className="h-10 sm:h-20" />

        {/* Contenedor relativo para hojas en triángulo */}
        <div className="hidden md:block relative w-28 h-20 ml-4">
          {/* Hoja 1: abajo izquierda */}
          <img
            src={hoja1}
            alt="Hoja 1"
            className="absolute bottom-0 left-0 h-10"
            style={{ zIndex: 1 }}
          />
          {/* Hoja 2: abajo derecha */}
          <img
            src={hoja2}
            alt="Hoja 2"
            className="absolute bottom-0 right-0 h-10"
            style={{ zIndex: 2 }}
          />
          {/* Hoja 3: centro arriba */}
          <img
            src={hoja3}
            alt="Hoja 3"
            className="absolute top-0 left-1/2 transform -translate-x-1/2 h-10"
            style={{ zIndex: 3 }}
          />
          {/* Hoja 4: ligeramente sobre posición de hoja 3 para profundidad */}
          <img
            src={hoja4}
            alt="Hoja 4"
            className="absolute top-4 left-1/2 transform -translate-x-1/2 h-8 opacity-80"
            style={{ zIndex: 0 }}
          />
        </div>
      </div>

      <nav className="flex flex-wrap justify-end gap-2 -mt-10">
        <Link
          to="/"
          className="bg-[#4a5568] text-white px-8 py-3 rounded-lg font-semibold text-lg min-w-[100px] inline-block text-center"
        >
          Inicio
        </Link>
        <Link
          to="/prendas"
          className="bg-[#4a5568] text-white px-8 py-3 rounded-lg font-semibold text-lg min-w-[100px] inline-block text-center"
        >
          Prendas
        </Link>
        <Link
          to="/clientes"
          className="bg-[#4a5568] text-white px-8 py-3 rounded-lg font-semibold text-lg min-w-[100px] inline-block text-center"
        >
          Clientes
        </Link>
        <Link
          to="/categorias"
          className="bg-[#4a5568] text-white px-8 py-3 rounded-lg font-semibold text-lg min-w-[100px] inline-block text-center"
        >
          Categorías
        </Link>
        <Link
          to="/ventas"
          className="bg-[#4a5568] text-white px-8 py-3 rounded-lg font-semibold text-lg min-w-[100px] inline-block text-center"
        >
          Ventas
        </Link>
        <Link
          to="/usuarias"
          className="bg-[#4a5568] text-white px-8 py-3 rounded-lg font-semibold text-lg min-w-[100px] inline-block text-center"
        >
          Usuarias
        </Link>
      </nav>
    </header>
  );
}
