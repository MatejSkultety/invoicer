<script setup>
import { computed, onBeforeUnmount, reactive, watch } from 'vue'
import { t } from '../../shared/i18n'

const MAX_LENGTHS = {
  name: 256,
  address: 256,
  city: 128,
  country: 128,
  main_contact: 256,
  additional_contact: 256,
  ico: 32,
  dic: 32,
  notes: 1024
}

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  client: {
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
  address: '',
  city: '',
  country: '',
  main_contact_method: 'email',
  main_contact: '',
  additional_contact: '',
  ico: '',
  dic: '',
  notes: '',
  favourite: false
})

const errors = reactive({
  name: '',
  address: '',
  city: '',
  country: '',
  main_contact_method: '',
  main_contact: '',
  additional_contact: '',
  ico: '',
  dic: '',
  notes: ''
})

const isEdit = computed(() => Boolean(props.client))
const modalTitle = computed(() =>
  isEdit.value ? t('clients.modal.titleEdit') : t('clients.modal.titleCreate')
)

function resetForm() {
  const source = props.client
  form.name = source ? source.name : ''
  form.address = source ? source.address : ''
  form.city = source ? source.city : ''
  form.country = source ? source.country : ''
  form.main_contact_method = source ? source.main_contact_method : 'email'
  form.main_contact = source ? source.main_contact : ''
  form.additional_contact = source ? source.additional_contact || '' : ''
  form.ico = source ? source.ico || '' : ''
  form.dic = source ? source.dic || '' : ''
  form.notes = source ? source.notes || '' : ''
  form.favourite = source ? Boolean(source.favourite) : false
  clearErrors()
}

function clearErrors() {
  errors.name = ''
  errors.address = ''
  errors.city = ''
  errors.country = ''
  errors.main_contact_method = ''
  errors.main_contact = ''
  errors.additional_contact = ''
  errors.ico = ''
  errors.dic = ''
  errors.notes = ''
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
  () => props.client,
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

function validate() {
  clearErrors()
  let valid = true

  const nameValue = form.name.trim()
  if (!nameValue) {
    errors.name = t('clients.validation.nameRequired')
    valid = false
  } else if (nameValue.length > MAX_LENGTHS.name) {
    errors.name = t('clients.validation.nameTooLong', { max: MAX_LENGTHS.name })
    valid = false
  }

  const addressValue = form.address.trim()
  if (!addressValue) {
    errors.address = t('clients.validation.addressRequired')
    valid = false
  } else if (addressValue.length > MAX_LENGTHS.address) {
    errors.address = t('clients.validation.addressTooLong', { max: MAX_LENGTHS.address })
    valid = false
  }

  const cityValue = form.city.trim()
  if (!cityValue) {
    errors.city = t('clients.validation.cityRequired')
    valid = false
  } else if (cityValue.length > MAX_LENGTHS.city) {
    errors.city = t('clients.validation.cityTooLong', { max: MAX_LENGTHS.city })
    valid = false
  }

  const countryValue = form.country.trim()
  if (!countryValue) {
    errors.country = t('clients.validation.countryRequired')
    valid = false
  } else if (countryValue.length > MAX_LENGTHS.country) {
    errors.country = t('clients.validation.countryTooLong', { max: MAX_LENGTHS.country })
    valid = false
  }

  if (!form.main_contact_method) {
    errors.main_contact_method = t('clients.validation.contactMethodRequired')
    valid = false
  }

  const mainContactValue = form.main_contact.trim()
  if (!mainContactValue) {
    errors.main_contact = t('clients.validation.mainContactRequired')
    valid = false
  } else if (mainContactValue.length > MAX_LENGTHS.main_contact) {
    errors.main_contact = t('clients.validation.mainContactTooLong', {
      max: MAX_LENGTHS.main_contact
    })
    valid = false
  }

  const additionalContactValue = form.additional_contact.trim()
  if (
    additionalContactValue &&
    additionalContactValue.length > MAX_LENGTHS.additional_contact
  ) {
    errors.additional_contact = t('clients.validation.additionalContactTooLong', {
      max: MAX_LENGTHS.additional_contact
    })
    valid = false
  }

  const icoValue = form.ico.trim()
  if (icoValue && icoValue.length > MAX_LENGTHS.ico) {
    errors.ico = t('clients.validation.icoTooLong', { max: MAX_LENGTHS.ico })
    valid = false
  }

  const dicValue = form.dic.trim()
  if (dicValue && dicValue.length > MAX_LENGTHS.dic) {
    errors.dic = t('clients.validation.dicTooLong', { max: MAX_LENGTHS.dic })
    valid = false
  }

  const notesValue = form.notes.trim()
  if (notesValue && notesValue.length > MAX_LENGTHS.notes) {
    errors.notes = t('clients.validation.notesTooLong', { max: MAX_LENGTHS.notes })
    valid = false
  }

  return valid
}

function close() {
  emit('update:modelValue', false)
}

function submit() {
  if (!validate()) {
    return
  }

  emit('submit', {
    name: form.name.trim(),
    address: form.address.trim(),
    city: form.city.trim(),
    country: form.country.trim(),
    main_contact_method: form.main_contact_method,
    main_contact: form.main_contact.trim(),
    additional_contact: form.additional_contact.trim(),
    ico: form.ico.trim(),
    dic: form.dic.trim(),
    notes: form.notes.trim(),
    favourite: form.favourite
  })
}
</script>

<template>
  <div v-if="modelValue" class="overlay" role="dialog" aria-modal="true">
    <div class="modal">
      <header>
        <div class="title">
          <h2>{{ modalTitle }}</h2>
          <button
            type="button"
            class="favourite-toggle"
            :class="{ active: form.favourite }"
            :aria-pressed="form.favourite"
            :aria-label="t('clients.hints.favourite')"
            :title="t('clients.hints.favourite')"
            @click="form.favourite = !form.favourite"
          >
            {{ form.favourite ? '★' : '☆' }}
          </button>
        </div>
        <div class="header-actions">
          <button type="submit" form="client-form" :disabled="submitting">
            {{ submitting ? t('common.saving') : isEdit ? t('common.save') : t('common.create') }}
          </button>
          <button type="button" class="close" :aria-label="t('common.cancel')" @click="close">✕</button>
        </div>
      </header>

      <form id="client-form" class="form" @submit.prevent="submit">
        <label class="field">
          <span class="field-label">{{ t('clients.fields.name') }}</span>
          <div class="field-control">
            <input v-model="form.name" name="name" type="text" autocomplete="name" maxlength="256" />
            <span v-if="errors.name" class="error">{{ errors.name }}</span>
          </div>
        </label>

        <label class="field">
          <span class="field-label">{{ t('clients.fields.address') }}</span>
          <div class="field-control">
            <input
              v-model="form.address"
              name="address"
              type="text"
              autocomplete="street-address"
              maxlength="256"
            />
            <span v-if="errors.address" class="error">{{ errors.address }}</span>
          </div>
        </label>

        <label class="field">
          <span class="field-label">{{ t('clients.fields.city') }}</span>
          <div class="field-control">
            <input
              v-model="form.city"
              name="city"
              type="text"
              autocomplete="address-level2"
              maxlength="128"
            />
            <span v-if="errors.city" class="error">{{ errors.city }}</span>
          </div>
        </label>

        <label class="field">
          <span class="field-label">{{ t('clients.fields.country') }}</span>
          <div class="field-control">
            <input
              v-model="form.country"
              name="country"
              type="text"
              autocomplete="country-name"
              maxlength="128"
            />
            <span v-if="errors.country" class="error">{{ errors.country }}</span>
          </div>
        </label>

        <label class="field">
          <span class="field-label">{{ t('clients.fields.mainContactMethod') }}</span>
          <div class="field-control inline">
            <select
              v-model="form.main_contact_method"
              name="main_contact_method"
              class="select-inline"
            >
              <option value="email">📧 {{ t('clients.contactMethods.email') }}</option>
              <option value="whatsapp">💬 {{ t('clients.contactMethods.whatsapp') }}</option>
              <option value="discord">🎮 {{ t('clients.contactMethods.discord') }}</option>
            </select>
            <span v-if="errors.main_contact_method" class="error">{{ errors.main_contact_method }}</span>
          </div>
        </label>

        <label class="field">
          <span class="field-label">{{ t('clients.fields.mainContact') }}</span>
          <div class="field-control">
            <input v-model="form.main_contact" name="main_contact" type="text" maxlength="256" />
            <span v-if="errors.main_contact" class="error">{{ errors.main_contact }}</span>
          </div>
        </label>

        <div class="optional">
          <p class="optional-title">{{ t('clients.modal.optional') }}</p>

          <label class="field">
            <span class="field-label">{{ t('clients.fields.additionalContact') }}</span>
            <div class="field-control">
              <input
                v-model="form.additional_contact"
                name="additional_contact"
                type="text"
                maxlength="256"
              />
              <span v-if="errors.additional_contact" class="error">
                {{ errors.additional_contact }}
              </span>
            </div>
          </label>

          <label class="field">
            <span class="field-label">{{ t('clients.fields.ico') }}</span>
            <div class="field-control">
              <input v-model="form.ico" name="ico" type="text" maxlength="32" />
              <span v-if="errors.ico" class="error">{{ errors.ico }}</span>
            </div>
          </label>

          <label class="field">
            <span class="field-label">{{ t('clients.fields.dic') }}</span>
            <div class="field-control">
              <input v-model="form.dic" name="dic" type="text" maxlength="32" />
              <span v-if="errors.dic" class="error">{{ errors.dic }}</span>
            </div>
          </label>

          <label class="field">
            <span class="field-label">{{ t('clients.fields.notes') }}</span>
            <div class="field-control">
              <textarea v-model="form.notes" name="notes" rows="4" maxlength="1024"></textarea>
              <span v-if="errors.notes" class="error">{{ errors.notes }}</span>
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

.field-control.inline {
  flex-direction: row;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
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

.select-inline {
  width: auto;
  min-width: 0;
}

select {
  background: #ffffff;
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

button.ghost {
  background: #e2e8f0;
  color: #1f2933;
}

button:disabled {
  opacity: 0.7;
  cursor: wait;
}

.favourite-toggle {
  border: none;
  background: #e5e7eb;
  font-size: 22px;
  cursor: pointer;
  line-height: 1;
  padding: 6px;
  color: #94a3b8;
  border-radius: 999px;
  box-shadow: inset 0 0 0 1px #e2e8f0;
}

.favourite-toggle.active {
  background: #ffffff;
  color: #f59e0b;
  animation: star-pop 240ms ease-out;
}

.favourite-toggle:hover {
  color: #f59e0b;
}

@keyframes star-pop {
  0% {
    transform: scale(0.8) rotate(-8deg);
  }
  60% {
    transform: scale(1.15) rotate(6deg);
  }
  100% {
    transform: scale(1) rotate(0deg);
  }
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

  .title {
    width: 100%;
    justify-content: space-between;
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
