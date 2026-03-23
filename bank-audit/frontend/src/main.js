import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Clients from './views/Clients.vue'
import Retraits from './views/Retraits.vue'
import Audit from './views/Audit.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/retraits' },
    { path: '/clients', component: Clients },
    { path: '/retraits', component: Retraits },
    { path: '/audit', component: Audit },
  ]
})

createApp(App).use(router).mount('#app')
