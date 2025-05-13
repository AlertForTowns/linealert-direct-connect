import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/meta-stream': {
        target: 'http://127.0.0.1:5007',  // Backend address for streaming
        changeOrigin: true,
        secure: false,
      },
      '/alert': {
        target: 'http://127.0.0.1:5007',  // Backend address for receiving alerts
        changeOrigin: true,
        secure: false,
      }
    }
  }
});
