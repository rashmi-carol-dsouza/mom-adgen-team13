import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

import fs from 'fs';
import path from 'path';

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    {
      name: 'generate-200-html',
      apply: 'build',
      closeBundle() {
        const distPath = path.resolve(__dirname, 'dist');
        const indexHtml = path.join(distPath, 'index.html');
        const copyTo = path.join(distPath, '200.html');

        if (fs.existsSync(indexHtml)) {
          fs.copyFileSync(indexHtml, copyTo);
          console.log('✅ 200.html generated');
        }
      }
    }
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
