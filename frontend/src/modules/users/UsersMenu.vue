<script setup>
import { onBeforeUnmount, ref, watch } from 'vue'
import { t } from '../../shared/i18n'
import { useToast } from '../../shared/toast'
import { getCurrentUser, updateCurrentUser } from './api'
import UserProfileModal from './UserProfileModal.vue'

const menuOpen = ref(false)
const modalOpen = ref(false)
const profile = ref(null)
const loadingProfile = ref(false)
const loadError = ref('')
const submitting = ref(false)
const submitError = ref('')
const menuRef = ref(null)

const { addToast } = useToast()

function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

function closeMenu() {
  menuOpen.value = false
}

function openProfile() {
  closeMenu()
  modalOpen.value = true
  loadProfile()
}

async function loadProfile() {
  loadingProfile.value = true
  loadError.value = ''
  submitError.value = ''
  try {
    profile.value = await getCurrentUser()
  } catch (error) {
    loadError.value = error.message || t('users.errors.load')
    profile.value = null
  } finally {
    loadingProfile.value = false
  }
}

async function handleSubmit(payload) {
  submitting.value = true
  submitError.value = ''
  try {
    profile.value = await updateCurrentUser(payload)
    addToast(t('users.toasts.updated'))
    modalOpen.value = false
  } catch (error) {
    submitError.value = error.message || t('users.errors.save')
  } finally {
    submitting.value = false
  }
}

function onDocumentClick(event) {
  if (!menuOpen.value) {
    return
  }
  if (menuRef.value && !menuRef.value.contains(event.target)) {
    menuOpen.value = false
  }
}

function onKeydown(event) {
  if (event.key === 'Escape') {
    menuOpen.value = false
  }
}

watch(menuOpen, (open) => {
  if (open) {
    document.addEventListener('click', onDocumentClick)
    document.addEventListener('keydown', onKeydown)
  } else {
    document.removeEventListener('click', onDocumentClick)
    document.removeEventListener('keydown', onKeydown)
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('click', onDocumentClick)
  document.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <div ref="menuRef" class="user-menu">
    <button
      type="button"
      class="menu-trigger"
      :aria-expanded="menuOpen"
      aria-haspopup="menu"
      :aria-label="t('users.menu.label')"
      @click="toggleMenu"
    >
      <span class="menu-icon" aria-hidden="true">⚙️</span>
    </button>
    <div v-if="menuOpen" class="menu" role="menu">
      <button type="button" class="menu-item" role="menuitem" @click="openProfile">
        {{ t('users.menu.profile') }}
      </button>
      <button type="button" class="menu-item" role="menuitem" disabled>
        {{ t('users.menu.logoutSoon') }}
      </button>
    </div>

    <teleport to="body">
      <UserProfileModal
        v-model="modalOpen"
        :profile="profile"
        :loading="loadingProfile"
        :submitting="submitting"
        :error-message="submitError"
        :load-error="loadError"
        @submit="handleSubmit"
      />
    </teleport>
  </div>
</template>

<style scoped>
.user-menu {
  position: relative;
  display: flex;
  align-items: center;
}

.menu-trigger {
  border: 1px solid #d1dae3;
  background: #ffffff;
  width: 38px;
  height: 38px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 18px;
  line-height: 1;
  transition: border-color 0.2s ease, background 0.2s ease, box-shadow 0.2s ease;
}

.menu-trigger:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.menu-trigger:focus-visible {
  outline: 2px solid #93c5fd;
  outline-offset: 2px;
  box-shadow: 0 0 0 3px rgba(147, 197, 253, 0.35);
}

.menu-icon {
  display: inline-flex;
  transform: translateY(-1px);
}

.menu {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  min-width: 180px;
  padding: 8px;
  box-shadow: 0 16px 30px rgba(15, 23, 42, 0.2);
  display: flex;
  flex-direction: column;
  gap: 6px;
  z-index: 5;
}

.menu-item {
  border: none;
  background: transparent;
  text-align: left;
  padding: 8px 10px;
  border-radius: 8px;
  font: inherit;
  cursor: pointer;
}

.menu-item:hover {
  background: #f1f5f9;
}

.menu-item:disabled {
  color: #94a3b8;
  cursor: not-allowed;
}
</style>
