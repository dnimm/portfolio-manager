import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/users': 'http://127.0.0.1:5000',
      '/portfolios': 'http://127.0.0.1:5000',
      '/securities': 'http://127.0.0.1:5000',
      '/trades': 'http://127.0.0.1:5000',
    },
  },
})