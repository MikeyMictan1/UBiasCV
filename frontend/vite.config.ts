import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react' // This might say 'plugin-react-swc' or 'compiler'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(), // Add this line!
  ],
  // Forward /api calls to the FastAPI backend during dev
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})