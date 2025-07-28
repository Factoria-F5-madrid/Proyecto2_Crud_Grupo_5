import maniqui from '@/assets/maniqui_1.png';
import tijeras from '@/assets/tijera_1.png';
import carreteHilo from '@/assets/hilo_1.png';
import botonNaranja from '@/assets/boton_1.png';
import botonNaranja2 from '@/assets/boton_2.png';
import botonRojo from '@/assets/boton_3.png';
import agujaHilo from '@/assets/aguja_2.png';
import telasRojas from '@/assets/tela_1.png';
import telasNaranjas from '@/assets/tela_2.png';
import AnimatedText from './AnimatedText.jsx';
import AnimatedAsset from '@/components/AnimatedAsset.jsx';
import { dashboardAPI, handleAPIError } from "@/services/api";

export default function Body() {
  return <main className="flex-1 bg-[#333333]">
    <div className="flex-grow align-middle w-full h-full">
      {/* --- 2. TEXTO CENTRAL --- */}
      <div className="absolute top-[55%] left-[40%] -translate-x-1/2 -translate-y-1/2 text-center z-20 w-full max-w-md px-6">
        
        {/* Se añade "text-white" para que sea visible sobre el fondo oscuro */}
        <AnimatedText 
          text="Aquí no empiezas de cero." 
          className="text-[#404040] text-3xl md:text-4xl lg:text-5xl font-custom"
        />
        
        {/* Se añade "text-white" también aquí */}
        <AnimatedText 
          text="Aquí sigues adelante" 
          className="text-[#404040] text-3xl md:text-4xl lg:text-5xl font-custom"
        />
      </div>

      {/* --- 3. ASSETS DECORATIVOS --- */}
      {/* Reemplazamos <img> por <AnimatedAsset> y añadimos props de animación */}
      <AnimatedAsset 
          src={maniqui} 
          alt="Maniquí" 
          className="absolute top-[20%] left-[5%] w-[25%] max-w-[300px] z-0" 
          yOffset={10} 
          duration={4} 
      />
      <AnimatedAsset 
          src={carreteHilo} 
          alt="Carrete de Hilo" 
          className="absolute top-[20%] left-[30%] w-[12%] max-w-[180px]" 
          yOffset={-8} 
          duration={3.5} 
      />
      <AnimatedAsset 
          src={tijeras} 
          alt="Tijeras" 
          className="absolute top-[20%] left-[45%] w-[15%] max-w-[220px] rotate-[-15deg]" 
          yOffset={12} 
          duration={5} 
      />
      <AnimatedAsset 
          src={botonNaranja} 
          alt="Botón Naranja" 
          className="absolute top-[20%] right-[25%] w-[12%] max-w-[150px]" 
          yOffset={-5} 
          duration={2.8} 
      />
      <AnimatedAsset 
          src={botonRojo} 
          alt="Botón Rojo" 
          className="absolute top-[12%] right-[10%] w-[13%] max-w-[150px]" 
          yOffset={10} 
          duration={3.2} 
      />
      <AnimatedAsset 
          src={botonNaranja2} 
          alt="Botón Naranja 2" 
          className="absolute top-[35%] right-[30%] w-[10%] max-w-[120px]" 
          yOffset={-10} 
          duration={4.5} 
      />
      <AnimatedAsset 
          src={agujaHilo} 
          alt="Aguja con Hilo" 
          className="absolute top-[50%] right-[8%] w-[12%] max-w-[100px] rotate-[15deg]" 
          yOffset={8} 
          duration={3.8} 
      />
      <AnimatedAsset 
          src={telasNaranjas} 
          alt="Telas Naranjas" 
          className="absolute bottom-[8%] left-[25%] w-[18%] max-w-[180px]" 
          yOffset={-12} 
          duration={5.5} 
      />
      <AnimatedAsset 
          src={telasRojas} 
          alt="Telas Rojas" 
          className="absolute bottom-[10%] right-[20%] w-[22%] max-w-[200px]" 
          yOffset={10} 
          duration={6} 
      />
    </div>
  </main>
}