import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      name: 'GmsUICore',
      fileName: 'index'
    },
    rollupOptions: {
      external: ['react', 'react-dom', 'tailwindcss'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
          tailwindcss: 'tailwindcss'
        }
      }
    }
  }
})
