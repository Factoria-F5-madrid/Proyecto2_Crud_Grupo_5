import { motion } from 'framer-motion';

const AnimatedAsset = ({ src, alt, className, yOffset = 20, duration = 6 }) => {
  return (
    <motion.img
      src={src}
      alt={alt}
      className={className}
      // Estado inicial (no es estrictamente necesario, pero es buena práctica)
      initial={{ y: 0 }}
      // Estado final de la animación
      animate={{ y: yOffset }}
      // Configuración de la transición para que sea infinita y suave
      transition={{
        duration: duration,       // Duración del ciclo de animación
        repeat: Infinity,         // Repetir la animación para siempre
        repeatType: 'mirror',     // Hace que la animación vaya y vuelva (sube y baja)
        ease: 'easeInOut',        // Curva de aceleración suave
      }}
    />
  );
};

export default AnimatedAsset;