import { ref } from 'vue'
import sharedEn from './en'
import clientsEn from '../../modules/clients/i18n/en'
import catalogEn from '../../modules/catalog_items/i18n/en'
import usersEn from '../../modules/users/i18n/en'

const messages = {
  en: {
    ...sharedEn,
    clients: clientsEn,
    catalog: catalogEn,
    users: usersEn
  }
}

const locale = ref('en')

function resolveMessage(messageTree, key) {
  return key.split('.').reduce((value, segment) => {
    if (!value || typeof value !== 'object') {
      return undefined
    }
    return value[segment]
  }, messageTree)
}

export function t(key, params = {}) {
  const message = resolveMessage(messages[locale.value], key)
  if (typeof message !== 'string') {
    if (import.meta?.env?.DEV) {
      // eslint-disable-next-line no-console
      console.warn(`[i18n] Missing translation for key: ${key}`)
    }
    return key
  }

  return Object.entries(params).reduce((text, [token, value]) => {
    return text.replaceAll(`{${token}}`, String(value))
  }, message)
}

export function setLocale(nextLocale) {
  if (messages[nextLocale]) {
    locale.value = nextLocale
  }
}

export function getLocale() {
  return locale.value
}
