import Navbar from "@/components/Navbar.jsx";
import Footer from "@/components/Footer.jsx";
import CategoriasBody from "@/components/CategoriasBody.jsx";

export default function Dashboard() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Navbar fijo o normal según tu diseño */}
      <Navbar />
      
      {/* Esta sección debe crecer y ocupar el espacio restante */}
      <main className="flex-grow">
        <CategoriasBody />
      </main>

      {/* Footer al final */}
      <Footer />
    </div>
  );
}
