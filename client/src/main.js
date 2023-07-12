import './assets/main.css'

// main.js
import { createApp } from 'vue'
import App from './App.vue'
import store from './store'  // import the store

createApp(App)
  .use(store)  // provide the store to the Vue application
  .mount('#app')

