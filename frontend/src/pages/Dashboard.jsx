import React, { useState, useEffect } from 'react';
import { FiMenu, FiX } from 'react-icons/fi';
import { motion, AnimatePresence } from 'framer-motion';
import logoTexto from '@/assets/FÉNIX.png';
import logoCirculo from '@/assets/fenix_logo_2.png';
import fondo from '@/assets/screen.jpg'

const ResponsiveSidebar = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 768) {
        setIsSidebarOpen(true);
      } else {
        setIsSidebarOpen(false);
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize();

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="flex h-screen bg-[gray-100]">
      <AnimatePresence>
        {isSidebarOpen && (
          <motion.div
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            exit={{ x: -300 }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            className="fixed inset-y-0 left-0 z-30 w-64 bg-white shadow-lg md:relative md:translate-x-0"
          >
            <div className="flex items-center justify-between p-4 border-b bg-[#EBEBEB]">
              <h2 className="text-xl font-semibold">Menú</h2>
              <button
                onClick={toggleSidebar}
                className="p-2 rounded-md md:hidden hover:bg-gray-200"
              >
                <FiX className="w-6 h-6" />
              </button>
            </div>
            <div className="bg-[#EBEBEB] h-screen">
              <nav className="p-9">
                <ul className="space-y-2">
                  <li>
                    <a href="#" className="block p-2 rounded-md hover:bg-gray-200">Inicio</a>
                  </li>
                  <li>
                    <a href="#" className="block p-2 rounded-md hover:bg-gray-200">Usuarias</a>
                  </li>
                  <li>
                    <a href="#" className="block p-2 rounded-md hover:bg-gray-200">Clientes</a>
                  </li>
                  <li>
                    <a href="#" className="block p-2 rounded-md hover:bg-gray-200">Ventas</a>
                  </li>
                  <li>
                    <a href="#" className="block p-2 rounded-md hover:bg-gray-200">Prendas</a>
                  </li>
                </ul>
              </nav>
          </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="flex flex-col flex-1 overflow-hidden">
        <header className="flex items-center justify-between px-6 py-4 bg-[#EBEBEB] border-b">
          <button
            onClick={toggleSidebar}
            className="p-2 rounded-md md:hidden hover:bg-gray-200"
          >
            <FiMenu className="w-6 h-6" />
          </button>
          <div className="flex items-center gap-2 sm:gap-3">
            <img src={logoCirculo} alt="Logo Fenix" className="h-20 sm:h-22" />
            <img src={logoTexto} alt="FENIX" className="h-10 sm:h-20" />
          </div>
        </header>
        <main 
          className="flex-1 p-6 overflow-auto"
          style={{
          backgroundImage: `url(${fondo})`,
          backgroundSize: "cover",
          backgroundPosition: "center"
          }}>
          <h2 className="mb-4 text-xl font-semibold">Content</h2>
          <p className="mb-4">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
          </p>
          <p>
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
          </p>
        </main>
      </div>
    </div>
  );
};

export default ResponsiveSidebar;