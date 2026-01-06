import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { useToast } from './shared/toast'
import { t } from './shared/i18n'

const app = createApp(App).use(router)
const { addToast } = useToast()
let lastErrorAt = 0

function notifyUnexpected(error) {
  const now = Date.now()
  if (now - lastErrorAt < 2000) {
    return
  }
  lastErrorAt = now
  // eslint-disable-next-line no-console
  console.error(error)
  addToast(t('common.unexpectedError'), 'error')
}

app.config.errorHandler = (err) => {
  notifyUnexpected(err)
}

window.addEventListener('unhandledrejection', (event) => {
  notifyUnexpected(event.reason)
})

window.addEventListener('error', (event) => {
  notifyUnexpected(event.error || event.message)
})

app.mount('#app')
