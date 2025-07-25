/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Tu fuente personalizada existente
      fontFamily: {
        'custom': ['Rosalia', 'serif']
      },
      // Animación y keyframes agregados
      animation: {
        fall: "fall 10s linear infinite",
      },
      keyframes: {
        fall: {
          "0%": { transform: "translateY(-100%) rotate(0deg)" },
          "100%": { transform: "translateY(100vh) rotate(360deg)" },
        },
      },
    },
  },
  plugins: [],
}