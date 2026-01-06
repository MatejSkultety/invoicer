<script setup>
import { computed, onMounted, ref, shallowRef } from 'vue'
import CatalogItemModal from './CatalogItemModal.vue'
import { archiveCatalogItem, createCatalogItem, listCatalogItems, updateCatalogItem } from './api'
import { useToast } from '../../shared/toast'
import { t } from '../../shared/i18n'

// Shallow ref keeps derived card formatting from recomputing on deep mutations.
const items = shallowRef([])
const loading = ref(false)
const errorMessage = ref('')
const modalOpen = ref(false)
const activeItem = ref(null)
const submitting = ref(false)
const formError = ref('')

const { addToast } = useToast()

async function loadItems() {
  loading.value = true
  errorMessage.value = ''
  try {
    items.value = await listCatalogItems()
  } catch (error) {
    errorMessage.value = error.message || t('catalog.errors.load')
  } finally {
    loading.value = false
  }
}

function openCreate() {
  activeItem.value = null
  formError.value = ''
  modalOpen.value = true
}

function openEdit(item) {
  activeItem.value = item
  formError.value = ''
  modalOpen.value = true
}

async function handleSubmit(payload) {
  submitting.value = true
  formError.value = ''

  try {
    if (activeItem.value) {
      await updateCatalogItem(activeItem.value.id, payload)
      addToast(t('catalog.toasts.updated'))
    } else {
      await createCatalogItem(payload)
      addToast(t('catalog.toasts.created'))
    }
    modalOpen.value = false
    await loadItems()
  } catch (error) {
    formError.value = error.message || t('catalog.errors.save')
  } finally {
    submitting.value = false
  }
}

async function handleArchive(item) {
  errorMessage.value = ''
  try {
    await archiveCatalogItem(item.id)
    addToast(t('catalog.toasts.archived'))
    await loadItems()
  } catch (error) {
    errorMessage.value = error.message || t('catalog.errors.archive')
  }
}

function formatUnitPrice(value) {
  const numberValue = Number(value)
  if (Number.isNaN(numberValue)) {
    return '0.00'
  }
  return (numberValue / 100).toFixed(2)
}

const itemCards = computed(() =>
  items.value.map((item) => {
    const descriptionText = item.description ? item.description.trim() : ''
    const priceLine = t('catalog.page.priceLine', {
      price: formatUnitPrice(item.unit_price),
      unit: item.unit
    })
    const taxLine =
      item.tax_rate === null || item.tax_rate === undefined
        ? ''
        : t('catalog.page.taxLine', { rate: item.tax_rate })
    return {
      ...item,
      descriptionText,
      priceLine,
      taxLine
    }
  })
)

onMounted(() => {
  loadItems()
})
</script>

<template>
  <section class="page">
    <header class="header">
      <div>
        <p class="eyebrow">{{ t('catalog.page.eyebrow') }}</p>
        <h1>{{ t('catalog.page.title') }}</h1>
      </div>
      <button class="primary" type="button" @click="openCreate">
        {{ t('catalog.page.actions.create') }}
      </button>
    </header>

    <CatalogItemModal
      v-model="modalOpen"
      :item="activeItem"
      :submitting="submitting"
      :error-message="formError"
      @submit="handleSubmit"
    />

    <div v-if="loading" class="state">{{ t('catalog.page.loading') }}</div>
    <div v-else-if="errorMessage" class="state error">
      <p>{{ errorMessage }}</p>
      <button type="button" class="ghost" @click="loadItems">
        {{ t('common.retry') }}
      </button>
    </div>
    <div v-else-if="items.length === 0" class="state">{{ t('catalog.page.empty') }}</div>

    <div v-else class="grid">
      <article v-for="item in itemCards" :key="item.id" class="card">
        <div class="card-header">
          <div class="title">
            <h2>{{ item.name }}</h2>
            <span class="price">{{ item.priceLine }}</span>
          </div>
          <div class="actions">
            <button type="button" class="ghost" @click="openEdit(item)">
              {{ t('catalog.page.actions.edit') }}
            </button>
            <button type="button" class="danger" @click="handleArchive(item)">
              {{ t('catalog.page.actions.archive') }}
            </button>
          </div>
        </div>
        <p
          class="meta description"
          :class="{ hidden: !item.descriptionText }"
          :aria-hidden="!item.descriptionText"
        >
          {{ item.descriptionText }}
        </p>
        <p v-if="item.taxLine" class="meta tax">{{ item.taxLine }}</p>
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

.price {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 2px 8px;
  border-radius: 999px;
  background: #e0f2fe;
  color: #0369a1;
  font-size: 12px;
  font-weight: 600;
}

.meta {
  margin: 0;
  color: #52606d;
  font-size: 14px;
}

.description {
  color: #1f2933;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.description.hidden {
  visibility: hidden;
}

.tax {
  font-size: 12px;
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
