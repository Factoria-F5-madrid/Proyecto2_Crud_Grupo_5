import Navbar from "@/components/Navbar.jsx";
import Footer from "@/components/Footer.jsx";
import PrendasBody from "@/components/PrendasBody";
import PrendasList from "@/components/PrendasList";

export default function Prendas() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Navbar fijo o normal según tu diseño */}
      <Navbar />
      
      {/* Esta sección debe crecer y ocupar el espacio restante */}
      <main className="flex-grow">
        <PrendasList /> 
        <PrendasBody />
      </main>

      {/* Footer al final */}
      <Footer />
    </div>
  );
}
