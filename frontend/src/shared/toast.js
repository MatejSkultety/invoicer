import { reactive } from 'vue'

const state = reactive({
  toasts: []
})

let nextId = 1

function removeToast(id) {
  const index = state.toasts.findIndex((toast) => toast.id === id)
  if (index >= 0) {
    state.toasts.splice(index, 1)
  }
}

function addToast(message, variant = 'success', duration = 2800) {
  const toast = {
    id: nextId,
    message,
    variant
  }
  nextId += 1
  state.toasts.push(toast)

  window.setTimeout(() => removeToast(toast.id), duration)
}

export function useToast() {
  return {
    state,
    addToast,
    removeToast
  }
}
