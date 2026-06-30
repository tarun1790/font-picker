/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          bg: '#080810',
          panel: '#0F0F1A',
          border: '#1A1A2E',
          primary: '#6366F1',
          secondary: '#10B981',
          accent: '#EC4899',
          muted: '#9CA3AF'
        }
      },
      fontFamily: {
        serif: ['Playfair Display', 'Lora', 'Georgia', 'serif'],
        sans: ['Inter', 'Roboto', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
