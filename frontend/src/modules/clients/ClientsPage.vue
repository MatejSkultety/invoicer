<script setup>
import { computed, onMounted, ref, shallowRef } from 'vue'
import ClientModal from './ClientModal.vue'
import { archiveClient, createClient, listClients, updateClient } from './api'
import { useToast } from '../../shared/toast'
import { t } from '../../shared/i18n'

// Shallow ref keeps derived card formatting from recomputing on deep mutations.
const clients = shallowRef([])
const loading = ref(false)
const errorMessage = ref('')
const modalOpen = ref(false)
const activeClient = ref(null)
const submitting = ref(false)
const formError = ref('')

const { addToast } = useToast()

const contactMeta = computed(() => ({
  email: { label: t('clients.contactMethods.email'), emoji: '📧' },
  whatsapp: { label: t('clients.contactMethods.whatsapp'), emoji: '💬' },
  discord: { label: t('clients.contactMethods.discord'), emoji: '🎮' }
}))

async function loadClients() {
  loading.value = true
  errorMessage.value = ''
  try {
    clients.value = await listClients()
  } catch (error) {
    errorMessage.value = error.message || t('clients.errors.load')
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
      addToast(t('clients.toasts.updated'))
    } else {
      await createClient(payload)
      addToast(t('clients.toasts.created'))
    }
    modalOpen.value = false
    await loadClients()
  } catch (error) {
    formError.value = error.message || t('clients.errors.save')
  } finally {
    submitting.value = false
  }
}

async function handleArchive(client) {
  errorMessage.value = ''
  try {
    await archiveClient(client.id)
    addToast(t('clients.toasts.archived'))
    await loadClients()
  } catch (error) {
    errorMessage.value = error.message || t('clients.errors.archive')
  }
}

function primaryContact(client) {
  const meta = contactMeta.value[client.main_contact_method] || {
    label: client.main_contact_method,
    emoji: '💬'
  }
  return `${meta.emoji} ${meta.label}: ${client.main_contact}`
}

onMounted(() => {
  loadClients()
})

const clientCards = computed(() =>
  clients.value.map((client) => ({
    ...client,
    contactLine: primaryContact(client),
    notesText: client.notes ? client.notes.trim() : ''
  }))
)
</script>

<template>
  <section class="page">
    <header class="header">
      <div>
        <p class="eyebrow">{{ t('clients.page.eyebrow') }}</p>
        <h1>{{ t('clients.page.title') }}</h1>
      </div>
      <button class="primary" type="button" @click="openCreate">
        {{ t('clients.page.actions.create') }}
      </button>
    </header>

    <ClientModal
      v-model="modalOpen"
      :client="activeClient"
      :submitting="submitting"
      :error-message="formError"
      @submit="handleSubmit"
    />

    <div v-if="loading" class="state">{{ t('clients.page.loading') }}</div>
    <div v-else-if="errorMessage" class="state error">
      <p>{{ errorMessage }}</p>
      <button type="button" class="ghost" @click="loadClients">
        {{ t('common.retry') }}
      </button>
    </div>
    <div v-else-if="clients.length === 0" class="state">{{ t('clients.page.empty') }}</div>

    <div v-else class="grid">
      <article v-for="client in clientCards" :key="client.id" class="card">
        <div class="card-header">
          <div class="title">
            <h2>{{ client.name }}</h2>
            <span v-if="client.favourite" class="badge">
              ⭐ {{ t('clients.page.badges.favourite') }}
            </span>
          </div>
          <div class="actions">
            <button type="button" class="ghost" @click="openEdit(client)">
              {{ t('clients.page.actions.edit') }}
            </button>
            <button type="button" class="danger" @click="handleArchive(client)">
              {{ t('clients.page.actions.archive') }}
            </button>
          </div>
        </div>
        <p class="meta contact">{{ client.contactLine }}</p>
        <p
          class="notes"
          :class="{ hidden: !client.notesText }"
          :aria-hidden="!client.notesText"
        >
          {{ client.notesText }}
        </p>
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

.title {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
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

.meta.contact {
  color: #1f2933;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notes {
  margin: 0;
  font-size: 14px;
  color: #1f2933;
  min-height: 1.2em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notes.hidden {
  visibility: hidden;
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

.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 2px 8px;
  border-radius: 999px;
  background: #fef3c7;
  color: #92400e;
  font-size: 12px;
  font-weight: 600;
}

@media (max-width: 640px) {
  .header {
    flex-direction: column;
    align-items: flex-start;
  }

  .primary {
    width: 100%;
    text-align: center;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .actions {
    width: 100%;
  }

  button.ghost,
  button.danger {
    flex: 1;
  }
}
</style>
