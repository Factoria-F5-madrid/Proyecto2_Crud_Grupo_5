import { motion } from 'framer-motion';

// Variante para el contenedor que orquesta la animación de los hijos
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { 
      staggerChildren: 0.20 // Controla el retraso entre cada palabra
    },
  },
};

// Variante para cada palabra individual
const childVariants = {
  hidden: {
    opacity: 0,
    y: 20, // Empieza 20px más abajo
  },
  visible: {
    opacity: 1,
    y: 0, // Sube a su posición final
    transition: {
      type: 'spring',
      stiffness: 100,
    },
  },
};

const AnimatedText = ({ text, className = '' }) => {
  // Dividimos el texto en un array de palabras
  const words = text.split(' ');

  return (
    <motion.div // Usamos motion.div como contenedor principal de la animación
      className={className}
      style={{ overflow: 'hidden' }} // Asegura que el texto que sube no se vea antes
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {words.map((word, index) => (
        <motion.span
          key={index}
          variants={childVariants}
          style={{ display: 'inline-block', marginRight: '0.4em' }} // Espacio entre palabras
        >
          {word}
        </motion.span>
      ))}
    </motion.div>
  );
};

export default AnimatedText;