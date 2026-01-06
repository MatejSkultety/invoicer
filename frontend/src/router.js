import { createRouter, createWebHistory } from 'vue-router'
import ClientsPage from './modules/clients/ClientsPage.vue'
import CatalogItemsPage from './modules/catalog_items/CatalogItemsPage.vue'

const routes = [
  { path: '/', redirect: '/clients' },
  { path: '/clients', component: ClientsPage },
  { path: '/catalog', component: CatalogItemsPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
