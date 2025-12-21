import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  css: {
    postcss: './postcss.config.cjs',
  },
  server:{
    allowedHosts:["relieved-parakeet-ghastly.ngrok-free.app","backend-1005385950490.us-central1.run.app"]
  }
})
