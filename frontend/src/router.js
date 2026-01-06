import { createRouter, createWebHistory } from 'vue-router'
import ClientsPage from './modules/clients/ClientsPage.vue'

const routes = [
  { path: '/', redirect: '/clients' },
  { path: '/clients', component: ClientsPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
