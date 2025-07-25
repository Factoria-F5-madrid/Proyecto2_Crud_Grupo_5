import Navbar from "@/components/Navbar.jsx";
import Footer from "@/components/Footer.jsx";
import ClientesBody from "@/components/ClientesBody.jsx";

export default function Dashboard() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Navbar fijo o normal según tu diseño */}
      <Navbar />
      
      {/* Esta sección debe crecer y ocupar el espacio restante */}
      <main className="flex-grow">
        <ClientesBody />
      </main>

      {/* Footer al final */}
      <Footer />
    </div>
  );
}
