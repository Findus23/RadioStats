import vue from '@vitejs/plugin-vue'
import {defineConfig} from 'vite'

export default defineConfig({
    plugins: [
        vue()
    ],
    server: {
        proxy: {
            "/api": "http://127.0.0.1:5000"
        }
    },
    build: {
        sourcemap: true,
        target: "es2019"
    }
})
