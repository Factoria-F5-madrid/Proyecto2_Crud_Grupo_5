import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path'; // <- Importa el módulo 'path'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'https://fenix-pbad.onrender.com/api'
    }
  },
  // Añade esta sección para resolver las rutas con @
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});