import {createVuePlugin} from 'vite-plugin-vue2'
import {defineConfig} from 'vite'

export default defineConfig({
    plugins: [
        createVuePlugin()
    ],
    server: {
        proxy: {
            "/api": "http://localhost:5000"
        }
    },
    build: {
        sourcemap: true,
        target: "es2019"
    }
})
