<script setup>
import { onMounted, ref } from 'vue'
import ClientModal from './ClientModal.vue'
import { archiveClient, createClient, listClients, updateClient } from './api'
import { useToast } from '../../shared/toast'

const clients = ref([])
const loading = ref(false)
const errorMessage = ref('')
const modalOpen = ref(false)
const activeClient = ref(null)
const submitting = ref(false)
const formError = ref('')

const { addToast } = useToast()

async function loadClients() {
  loading.value = true
  errorMessage.value = ''
  try {
    clients.value = await listClients()
  } catch (error) {
    errorMessage.value = error.message || 'Unable to load clients.'
  } finally {
    loading.value = false
  }
}

function openCreate() {
  activeClient.value = null
  formError.value = ''
  modalOpen.value = true
}

function openEdit(client) {
  activeClient.value = client
  formError.value = ''
  modalOpen.value = true
}

async function handleSubmit(payload) {
  submitting.value = true
  formError.value = ''

  try {
    if (activeClient.value) {
      await updateClient(activeClient.value.id, payload)
      addToast('Client updated')
    } else {
      await createClient(payload)
      addToast('Client created')
    }
    modalOpen.value = false
    await loadClients()
  } catch (error) {
    formError.value = error.message || 'Unable to save client.'
  } finally {
    submitting.value = false
  }
}

async function handleArchive(client) {
  errorMessage.value = ''
  try {
    await archiveClient(client.id)
    addToast('Client archived')
    await loadClients()
  } catch (error) {
    errorMessage.value = error.message || 'Unable to archive client.'
  }
}

function notesPreview(notes) {
  const trimmed = notes.trim()
  if (trimmed.length <= 120) {
    return trimmed
  }
  return `${trimmed.slice(0, 120)}...`
}

onMounted(() => {
  loadClients()
})
</script>

<template>
  <section class="page">
    <header class="header">
      <div>
        <p class="eyebrow">Clients</p>
        <h1>Manage your clients</h1>
      </div>
      <button class="primary" type="button" @click="openCreate">Create client</button>
    </header>

    <ClientModal
      v-model="modalOpen"
      :client="activeClient"
      :submitting="submitting"
      :error-message="formError"
      @submit="handleSubmit"
    />

    <div v-if="loading" class="state">Loading clients...</div>
    <div v-else-if="errorMessage" class="state error">
      <p>{{ errorMessage }}</p>
      <button type="button" class="ghost" @click="loadClients">Retry</button>
    </div>
    <div v-else-if="clients.length === 0" class="state">No clients yet.</div>

    <div v-else class="grid">
      <article v-for="client in clients" :key="client.id" class="card">
        <div class="card-header">
          <h2>{{ client.name }}</h2>
          <div class="actions">
            <button type="button" class="ghost" @click="openEdit(client)">Edit</button>
            <button type="button" class="danger" @click="handleArchive(client)">Archive</button>
          </div>
        </div>
        <p class="meta">{{ client.email }}</p>
        <p class="meta">{{ client.address }}</p>
        <p class="notes">{{ notesPreview(client.notes) }}</p>
      </article>
    </div>
  </section>
</template>

<style scoped>
.page {
  max-width: 960px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 12px;
  color: #52606d;
  margin: 0 0 6px;
}

h1 {
  margin: 0;
  font-size: 28px;
}

.primary {
  border: none;
  border-radius: 999px;
  padding: 10px 18px;
  font-weight: 600;
  background: #2563eb;
  color: #ffffff;
  cursor: pointer;
}

.state {
  background: rgba(255, 255, 255, 0.7);
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #dde4ed;
}

.state.error {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  background: #fef2f2;
  border-color: #fecaca;
  color: #991b1b;
}

.grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
}

.card {
  background: #ffffff;
  border-radius: 16px;
  padding: 18px;
  border: 1px solid #e1e8f0;
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.08);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

h2 {
  margin: 0;
  font-size: 18px;
}

.meta {
  margin: 0;
  color: #52606d;
  font-size: 14px;
}

.notes {
  margin: 0;
  font-size: 14px;
  color: #1f2933;
}

.actions {
  display: flex;
  gap: 8px;
}

button.ghost {
  border: 1px solid #cbd5e1;
  background: transparent;
  border-radius: 999px;
  padding: 6px 12px;
  cursor: pointer;
  font-size: 12px;
}

button.danger {
  border: none;
  background: #fee2e2;
  color: #991b1b;
  border-radius: 999px;
  padding: 6px 12px;
  cursor: pointer;
  font-size: 12px;
}
</style>
