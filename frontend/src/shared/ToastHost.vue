<script setup>
import { useToast } from './toast'
import { t } from './i18n'

const { state, removeToast } = useToast()
</script>

<template>
  <div class="toast-host" aria-live="polite">
    <div
      v-for="toast in state.toasts"
      :key="toast.id"
      class="toast"
      :class="toast.variant"
    >
      <span>{{ toast.message }}</span>
      <button type="button" @click="removeToast(toast.id)">{{ t('common.close') }}</button>
    </div>
  </div>
</template>

<style scoped>
.toast-host {
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 20;
}

.toast {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #1f2933;
  color: #f8fafc;
  border-radius: 12px;
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.2);
}

.toast.success {
  background: #1b4332;
}

.toast.error {
  background: #991b1b;
}

.toast button {
  border: none;
  background: transparent;
  color: inherit;
  font-size: 12px;
  cursor: pointer;
}

@media (max-width: 640px) {
  .toast-host {
    left: 20px;
    right: 20px;
    bottom: 20px;
  }

  .toast {
    justify-content: space-between;
  }
}
</style>
