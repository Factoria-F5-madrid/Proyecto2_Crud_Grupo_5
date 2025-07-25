import Navbar from "@/components/Navbar.jsx";
import Footer from "@/components/Footer.jsx";
import UsuariasBody from "@/components/UsuariasBody.jsx";

export default function Dashboard() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Navbar fijo o normal según tu diseño */}
      <Navbar />
      
      {/* Esta sección debe crecer y ocupar el espacio restante */}
      <main className="flex-grow">
        <UsuariasBody />
      </main>

      {/* Footer al final */}
      <Footer />
    </div>
  );
}
