// Plugins
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import eslint from 'vite-plugin-eslint'

// Utilities
import { defineConfig } from 'vite'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  base: '/static/',
  plugins: [
    vue(),
    // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
    vuetify({
      autoImport: true,
    }),
    eslint({
      include: ['src/**/*.ts', 'src/**/*.vue', 'src/*.ts', 'src/*.vue'],
    }),
  ],
  define: { 'process.env': {} },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
    extensions: [
      '.js',
      '.json',
      '.jsx',
      '.mjs',
      '.ts',
      '.tsx',
      '.vue',
    ],
  },
  server: {
    port: 5173,
  },
  build: {
    manifest: "manifest.json",
    outDir: path.resolve("./theme/dist"),
    rollupOptions: {
      input: {
        main: path.resolve("./theme/src/main.js"),
      }
    }
  }
})
