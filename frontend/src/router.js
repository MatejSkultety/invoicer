import { createRouter, createWebHistory } from 'vue-router'
import HomePage from './modules/home/HomePage.vue'
import ClientsPage from './modules/clients/ClientsPage.vue'
import CatalogItemsPage from './modules/catalog_items/CatalogItemsPage.vue'
import SetupProfilePage from './modules/users/SetupProfilePage.vue'
import { hasCompleteProfile, refreshProfileStatus } from './modules/users/profile'

const routes = [
  { path: '/', component: HomePage },
  { path: '/setup', component: SetupProfilePage, meta: { hideChrome: true } },
  { path: '/clients', component: ClientsPage },
  { path: '/catalog', component: CatalogItemsPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to) => {
  const ready = to.path === '/setup'
    ? await refreshProfileStatus()
    : await hasCompleteProfile()

  if (to.path === '/setup') {
    if (ready) {
      return { path: '/' }
    }
    return true
  }

  if (!ready) {
    return { path: '/setup' }
  }

  return true
})

export default router
