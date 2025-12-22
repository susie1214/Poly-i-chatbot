import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    allowedHosts: [
      'untheologically-unrecordable-ami.ngrok-free.dev'
    ],
    proxy: {
      '/generate': {
        target: 'http://localhost:5001',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path
      },
      '/embed': {
        target: 'http://localhost:5001',
        changeOrigin: true,
        secure: false
      },
      '/health': {
        target: 'http://localhost:5001',
        changeOrigin: true,
        secure: false
      },
      '/info': {
        target: 'http://localhost:5001',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
