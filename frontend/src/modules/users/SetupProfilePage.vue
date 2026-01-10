<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { t } from '../../shared/i18n'
import { useToast } from '../../shared/toast'
import UserProfileModal from './UserProfileModal.vue'
import { getCurrentUser, updateCurrentUser } from './api'
import { emptyProfile, isProfileComplete, normalizeProfile, refreshProfileStatus } from './profile'

const router = useRouter()
const { addToast } = useToast()

const modalOpen = ref(true)
const profile = ref(emptyProfile())
const loading = ref(false)
const loadError = ref('')
const submitting = ref(false)
const submitError = ref('')

async function loadProfile() {
  loading.value = true
  loadError.value = ''
  submitError.value = ''

  try {
    const data = await getCurrentUser()
    if (isProfileComplete(data)) {
      router.replace('/')
      return
    }
    profile.value = normalizeProfile(data)
  } catch (error) {
    if (error && error.status === 404) {
      profile.value = emptyProfile()
      return
    }
    loadError.value = error.message || t('users.errors.load')
    profile.value = emptyProfile()
  } finally {
    loading.value = false
  }
}

async function handleSubmit(payload) {
  submitting.value = true
  submitError.value = ''

  try {
    await updateCurrentUser(payload)
    await refreshProfileStatus()
    addToast(t('users.toasts.updated'))
    router.replace('/')
  } catch (error) {
    submitError.value = error.message || t('users.errors.save')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>

<template>
  <teleport to="body">
    <UserProfileModal
      v-model="modalOpen"
      :profile="profile"
      :loading="loading"
      :submitting="submitting"
      :error-message="submitError"
      :load-error="loadError"
      :closable="false"
      @submit="handleSubmit"
    />
  </teleport>
</template>
