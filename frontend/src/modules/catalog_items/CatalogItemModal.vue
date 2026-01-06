<script setup>
import { computed, onBeforeUnmount, reactive, watch } from 'vue'
import { t } from '../../shared/i18n'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  item: {
    type: Object,
    default: null
  },
  submitting: {
    type: Boolean,
    default: false
  },
  errorMessage: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'submit'])

const form = reactive({
  name: '',
  description: '',
  unit: '',
  unit_price: '',
  tax_rate: ''
})

const errors = reactive({
  name: '',
  description: '',
  unit: '',
  unit_price: '',
  tax_rate: ''
})

const isEdit = computed(() => Boolean(props.item))
const modalTitle = computed(() =>
  isEdit.value ? t('catalog.modal.titleEdit') : t('catalog.modal.titleCreate')
)
function formatUnitPrice(value) {
  if (typeof value !== 'number' || Number.isNaN(value)) {
    return ''
  }
  return (value / 100).toFixed(2)
}

function resetForm() {
  const source = props.item
  form.name = source ? source.name : ''
  form.description = source ? source.description : ''
  form.unit = source ? source.unit : ''
  form.unit_price = source ? formatUnitPrice(source.unit_price) : ''
  form.tax_rate = source && source.tax_rate !== null && source.tax_rate !== undefined
    ? String(source.tax_rate)
    : ''
  clearErrors()
}

function clearErrors() {
  errors.name = ''
  errors.description = ''
  errors.unit = ''
  errors.unit_price = ''
  errors.tax_rate = ''
}

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      resetForm()
      window.addEventListener('keydown', onKeydown)
    } else {
      window.removeEventListener('keydown', onKeydown)
    }
  }
)

watch(
  () => props.item,
  () => {
    if (props.modelValue) {
      resetForm()
    }
  }
)

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
})

function onKeydown(event) {
  if (event.key === 'Escape') {
    close()
  }
}

function normalizeDecimal(value) {
  return value.trim().replace(',', '.')
}

function normalizeTaxRateOnBlur() {
  const raw = String(form.tax_rate ?? '').trim()
  if (!raw) {
    return
  }
  const normalized = raw.replace(/\s+/g, '')
  const stripped = normalized.endsWith('%') ? normalized.slice(0, -1) : normalized
  if (!stripped) {
    return
  }
  if (!/^\d+$/.test(stripped)) {
    return
  }
  form.tax_rate = `${Number(stripped)}%`
}

function normalizeUnitPriceOnBlur() {
  const raw = String(form.unit_price ?? '').trim()
  if (!raw) {
    return
  }
  const normalized = normalizeDecimal(raw)
  const numberValue = Number(normalized)
  if (!Number.isFinite(numberValue) || numberValue < 0) {
    return
  }
  form.unit_price = numberValue.toFixed(2)
}

function parseUnitPrice(value) {
  const normalized = normalizeDecimal(String(value ?? ''))
  if (!normalized) {
    return null
  }
  if (!/^\d+(?:\.\d{0,2})?$/.test(normalized)) {
    return undefined
  }
  const [whole, fraction = ''] = normalized.split('.')
  return Number(whole) * 100 + Number(fraction.padEnd(2, '0'))
}

function parseTaxRate(value) {
  const trimmed = String(value ?? '').trim()
  if (!trimmed) {
    return null
  }
  const normalized = trimmed.replace(/\s+/g, '')
  const stripped = normalized.endsWith('%') ? normalized.slice(0, -1) : normalized
  if (!stripped) {
    return null
  }
  if (!/^\d+$/.test(stripped)) {
    return undefined
  }
  return Number(stripped)
}

function validate() {
  clearErrors()
  let valid = true

  if (!form.name.trim()) {
    errors.name = t('catalog.validation.nameRequired')
    valid = false
  }

  if (!form.description.trim()) {
    errors.description = t('catalog.validation.descriptionRequired')
    valid = false
  }

  if (!form.unit.trim()) {
    errors.unit = t('catalog.validation.unitRequired')
    valid = false
  }

  const parsedPrice = parseUnitPrice(form.unit_price)
  if (parsedPrice === null) {
    errors.unit_price = t('catalog.validation.unitPriceRequired')
    valid = false
  } else if (parsedPrice === undefined) {
    errors.unit_price = t('catalog.validation.unitPriceInvalid')
    valid = false
  }

  const parsedTax = parseTaxRate(form.tax_rate)
  if (parsedTax === undefined) {
    errors.tax_rate = t('catalog.validation.taxRateInvalid')
    valid = false
  }

  return { valid, parsedPrice, parsedTax }
}

function close() {
  emit('update:modelValue', false)
}

function submit() {
  const { valid, parsedPrice, parsedTax } = validate()
  if (!valid) {
    return
  }

  emit('submit', {
    name: form.name.trim(),
    description: form.description.trim(),
    unit: form.unit.trim(),
    unit_price: parsedPrice,
    tax_rate: parsedTax
  })
}
</script>

<template>
  <div v-if="modelValue" class="overlay" role="dialog" aria-modal="true">
    <div class="modal">
      <header>
        <div class="title">
          <h2>{{ modalTitle }}</h2>
        </div>
        <div class="header-actions">
          <button type="submit" form="catalog-form" :disabled="submitting">
            {{ submitting ? t('common.saving') : isEdit ? t('common.save') : t('common.create') }}
          </button>
          <button type="button" class="close" :aria-label="t('common.cancel')" @click="close">
            ✕
          </button>
        </div>
      </header>

      <form id="catalog-form" class="form" @submit.prevent="submit">
        <label class="field">
          <span class="field-label">{{ t('catalog.fields.name') }}</span>
          <div class="field-control">
            <input v-model="form.name" name="name" type="text" autocomplete="off" />
            <span v-if="errors.name" class="error">{{ errors.name }}</span>
          </div>
        </label>

        <label class="field">
          <span class="field-label">{{ t('catalog.fields.description') }}</span>
          <div class="field-control">
            <textarea v-model="form.description" name="description" rows="3"></textarea>
            <span v-if="errors.description" class="error">{{ errors.description }}</span>
          </div>
        </label>

        <label class="field">
          <span class="field-label">{{ t('catalog.fields.unit') }}</span>
          <div class="field-control">
            <input v-model="form.unit" name="unit" type="text" autocomplete="off" />
            <span v-if="errors.unit" class="error">{{ errors.unit }}</span>
          </div>
        </label>

        <label class="field">
          <span class="field-label">{{ t('catalog.fields.unitPrice') }}</span>
          <div class="field-control">
            <input
              v-model="form.unit_price"
              name="unit_price"
              type="text"
              inputmode="decimal"
              placeholder="0.00"
              autocomplete="off"
              @blur="normalizeUnitPriceOnBlur"
            />
            <span v-if="errors.unit_price" class="error">{{ errors.unit_price }}</span>
          </div>
        </label>

        <div class="optional">
          <p class="optional-title">{{ t('catalog.modal.optional') }}</p>

          <label class="field">
            <span class="field-label">{{ t('catalog.fields.taxRate') }}</span>
            <div class="field-control">
              <input
                v-model="form.tax_rate"
                name="tax_rate"
                type="text"
                inputmode="numeric"
                placeholder="21%"
                autocomplete="off"
                @blur="normalizeTaxRateOnBlur"
              />
              <span v-if="errors.tax_rate" class="error">{{ errors.tax_rate }}</span>
            </div>
          </label>
        </div>

        <p v-if="errorMessage" class="error-banner">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 10;
}

.modal {
  width: min(720px, 100%);
  max-width: 100%;
  max-height: 90vh;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.25);
  padding: 22px;
  display: flex;
  flex-direction: column;
  overflow-y: hidden;
  overflow-x: hidden;
}

header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.title {
  display: flex;
  align-items: center;
  gap: 8px;
}

h2 {
  margin: 0;
  font-size: 20px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.close {
  border: none;
  background: #e2e8f0;
  color: #1f2933;
  font-size: 16px;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border-radius: 999px;
}

.form {
  display: grid;
  gap: 12px;
  overflow-y: auto;
  padding-right: 4px;
  flex: 1;
  min-height: 0;
  overflow-x: hidden;
}

.field {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
  font-size: 14px;
}

.field-label {
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 12px;
  color: #6b7280;
  width: 120px;
}

.field-control {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  min-width: 0;
}

input,
textarea,
select {
  border: 1px solid #d2dae3;
  border-radius: 10px;
  padding: 10px 12px;
  font: inherit;
  width: 100%;
  box-sizing: border-box;
}

textarea {
  resize: none;
}

.error {
  color: #b91c1c;
  font-size: 12px;
}

.error-banner {
  background: #fee2e2;
  color: #991b1b;
  padding: 10px 12px;
  border-radius: 10px;
  font-size: 13px;
  margin: 0;
}

.optional {
  border: 1px solid #e5e7eb;
  background: #f8fafc;
  border-radius: 12px;
  padding: 12px;
  display: grid;
  gap: 12px;
}

.optional-title {
  margin: 0;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #6b7280;
}

button {
  border: none;
  border-radius: 10px;
  padding: 10px 16px;
  font: inherit;
  cursor: pointer;
  background: #2563eb;
  color: #ffffff;
}

button:disabled {
  opacity: 0.7;
  cursor: wait;
}

@media (max-width: 640px) {
  .overlay {
    padding: 0;
    align-items: stretch;
  }

  .modal {
    padding: 18px;
    width: 100%;
    height: 100vh;
    max-height: 100vh;
    border-radius: 0;
  }

  header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .form {
    padding-right: 0;
  }

  .field {
    align-items: flex-start;
    flex-direction: column;
  }

  .field-label {
    width: auto;
  }
}
</style>
