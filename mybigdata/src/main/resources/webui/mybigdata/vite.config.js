import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    open: true, // 在服务器启动时自动在浏览器中打开应用程序
    //host: 'localhost',  // 指定服务器主机名
    port: 3000, // 指定服务器端口
    proxy: { // 为开发服务器配置自定义代理规则
    }
  }
})
