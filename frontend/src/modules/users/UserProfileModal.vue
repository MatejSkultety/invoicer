<script setup>
import { computed, onBeforeUnmount, reactive, watch } from 'vue'
import { t } from '../../shared/i18n'

const MAX_LENGTHS = {
  name: 256,
  address: 256,
  city: 128,
  country: 128,
  trade_licensing_office: 256,
  ico: 32,
  dic: 32,
  email: 256,
  phone: 64,
  bank: 256,
  iban: 34,
  swift: 11
}

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  profile: {
    type: Object,
    default: null
  },
  closable: {
    type: Boolean,
    default: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  submitting: {
    type: Boolean,
    default: false
  },
  errorMessage: {
    type: String,
    default: ''
  },
  loadError: {
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
  trade_licensing_office: '',
  ico: '',
  dic: '',
  email: '',
  phone: '',
  bank: '',
  iban: '',
  swift: ''
})

const errors = reactive({
  name: '',
  address: '',
  city: '',
  country: '',
  trade_licensing_office: '',
  ico: '',
  dic: '',
  email: '',
  phone: '',
  bank: '',
  iban: '',
  swift: ''
})

const canEdit = computed(() => Boolean(props.profile) && !props.loading && !props.loadError)

function resetForm() {
  const source = props.profile
  form.name = source?.name ?? ''
  form.address = source?.address ?? ''
  form.city = source?.city ?? ''
  form.country = source?.country ?? ''
  form.trade_licensing_office = source?.trade_licensing_office ?? ''
  form.ico = source?.ico ?? ''
  form.dic = source?.dic ?? ''
  form.email = source?.email ?? ''
  form.phone = source?.phone ?? ''
  form.bank = source?.bank ?? ''
  form.iban = source?.iban ?? ''
  form.swift = source?.swift ?? ''
  clearErrors()
}

function clearErrors() {
  errors.name = ''
  errors.address = ''
  errors.city = ''
  errors.country = ''
  errors.trade_licensing_office = ''
  errors.ico = ''
  errors.dic = ''
  errors.email = ''
  errors.phone = ''
  errors.bank = ''
  errors.iban = ''
  errors.swift = ''
}

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      resetForm()
      if (props.closable) {
        window.addEventListener('keydown', onKeydown)
      }
    } else {
      window.removeEventListener('keydown', onKeydown)
    }
  }
)

watch(
  () => props.profile,
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
  if (event.key === 'Escape' && props.closable) {
    close()
  }
}

function validate() {
  clearErrors()
  let valid = true

  const checks = [
    ['name', MAX_LENGTHS.name, 'users.validation.nameRequired', 'users.validation.nameTooLong'],
    ['address', MAX_LENGTHS.address, 'users.validation.addressRequired', 'users.validation.addressTooLong'],
    ['city', MAX_LENGTHS.city, 'users.validation.cityRequired', 'users.validation.cityTooLong'],
    ['country', MAX_LENGTHS.country, 'users.validation.countryRequired', 'users.validation.countryTooLong'],
    [
      'trade_licensing_office',
      MAX_LENGTHS.trade_licensing_office,
      'users.validation.tradeLicensingOfficeRequired',
      'users.validation.tradeLicensingOfficeTooLong'
    ],
    ['ico', MAX_LENGTHS.ico, 'users.validation.icoRequired', 'users.validation.icoTooLong'],
    ['dic', MAX_LENGTHS.dic, 'users.validation.dicRequired', 'users.validation.dicTooLong'],
    ['email', MAX_LENGTHS.email, 'users.validation.emailRequired', 'users.validation.emailTooLong'],
    ['phone', MAX_LENGTHS.phone, 'users.validation.phoneRequired', 'users.validation.phoneTooLong'],
    ['bank', MAX_LENGTHS.bank, 'users.validation.bankRequired', 'users.validation.bankTooLong'],
    ['iban', MAX_LENGTHS.iban, 'users.validation.ibanRequired', 'users.validation.ibanTooLong'],
    ['swift', MAX_LENGTHS.swift, 'users.validation.swiftRequired', 'users.validation.swiftTooLong']
  ]

  checks.forEach(([field, max, requiredKey, tooLongKey]) => {
    const value = form[field].trim()
    if (!value) {
      errors[field] = t(requiredKey)
      valid = false
      return
    }
    if (value.length > max) {
      errors[field] = t(tooLongKey, { max })
      valid = false
    }
  })

  return valid
}

function close() {
  if (!props.closable) {
    return
  }
  emit('update:modelValue', false)
}

function submit() {
  if (!canEdit.value) {
    return
  }
  if (!validate()) {
    return
  }

  emit('submit', {
    name: form.name.trim(),
    address: form.address.trim(),
    city: form.city.trim(),
    country: form.country.trim(),
    trade_licensing_office: form.trade_licensing_office.trim(),
    ico: form.ico.trim(),
    dic: form.dic.trim(),
    email: form.email.trim(),
    phone: form.phone.trim(),
    bank: form.bank.trim(),
    iban: form.iban.trim(),
    swift: form.swift.trim()
  })
}
</script>

<template>
  <div v-if="modelValue" class="overlay" role="dialog" aria-modal="true">
    <div class="modal">
      <header>
        <div class="title">
          <h2>{{ t('users.modal.title') }}</h2>
          <span v-if="loading" class="status">{{ t('users.modal.loading') }}</span>
        </div>
        <div class="header-actions">
          <button type="submit" form="user-profile-form" :disabled="submitting || !canEdit">
            {{ submitting ? t('common.saving') : t('common.save') }}
          </button>
          <button
            v-if="closable"
            type="button"
            class="close"
            :aria-label="t('common.cancel')"
            @click="close"
          >
            ✕
          </button>
        </div>
      </header>

      <form id="user-profile-form" class="form" @submit.prevent="submit">
        <p v-if="loadError" class="error-banner">{{ loadError }}</p>

        <p class="section-title">{{ t('users.modal.allRequired') }}</p>

        <label class="field">
          <span class="field-label">{{ t('users.fields.name') }}</span>
          <div class="field-control">
            <input
              v-model="form.name"
              name="name"
              type="text"
              autocomplete="name"
              maxlength="256"
              :disabled="!canEdit"
            />
            <span v-if="errors.name" class="error">{{ errors.name }}</span>
          </div>
        </label>

        <label class="field">
          <span class="field-label">{{ t('users.fields.address') }}</span>
          <div class="field-control">
            <input
              v-model="form.address"
              name="address"
              type="text"
              autocomplete="street-address"
              maxlength="256"
              :disabled="!canEdit"
            />
            <span v-if="errors.address" class="error">{{ errors.address }}</span>
          </div>
        </label>

        <label class="field">
          <span class="field-label">{{ t('users.fields.city') }}</span>
          <div class="field-control">
            <input
              v-model="form.city"
              name="city"
              type="text"
              autocomplete="address-level2"
              maxlength="128"
              :disabled="!canEdit"
            />
            <span v-if="errors.city" class="error">{{ errors.city }}</span>
          </div>
        </label>

        <label class="field">
          <span class="field-label">{{ t('users.fields.country') }}</span>
          <div class="field-control">
            <input
              v-model="form.country"
              name="country"
              type="text"
              autocomplete="country-name"
              maxlength="128"
              :disabled="!canEdit"
            />
            <span v-if="errors.country" class="error">{{ errors.country }}</span>
          </div>
        </label>

        <label class="field">
          <span class="field-label">{{ t('users.fields.tradeLicensingOffice') }}</span>
          <div class="field-control">
            <input
              v-model="form.trade_licensing_office"
              name="trade_licensing_office"
              type="text"
              maxlength="256"
              :disabled="!canEdit"
            />
            <span v-if="errors.trade_licensing_office" class="error">
              {{ errors.trade_licensing_office }}
            </span>
          </div>
        </label>

        <div class="section">
          <p class="section-title">{{ t('users.modal.details') }}</p>

          <label class="field">
            <span class="field-label">{{ t('users.fields.ico') }}</span>
            <div class="field-control">
              <input
                v-model="form.ico"
                name="ico"
                type="text"
                maxlength="32"
                :disabled="!canEdit"
              />
              <span v-if="errors.ico" class="error">{{ errors.ico }}</span>
            </div>
          </label>

          <label class="field">
            <span class="field-label">{{ t('users.fields.dic') }}</span>
            <div class="field-control">
              <input
                v-model="form.dic"
                name="dic"
                type="text"
                maxlength="32"
                :disabled="!canEdit"
              />
              <span v-if="errors.dic" class="error">{{ errors.dic }}</span>
            </div>
          </label>

          <label class="field">
            <span class="field-label">{{ t('users.fields.email') }}</span>
            <div class="field-control">
              <input
                v-model="form.email"
                name="email"
                type="email"
                autocomplete="email"
                maxlength="256"
                :disabled="!canEdit"
              />
              <span v-if="errors.email" class="error">{{ errors.email }}</span>
            </div>
          </label>

          <label class="field">
            <span class="field-label">{{ t('users.fields.phone') }}</span>
            <div class="field-control">
              <input
                v-model="form.phone"
                name="phone"
                type="tel"
                autocomplete="tel"
                maxlength="64"
                :disabled="!canEdit"
              />
              <span v-if="errors.phone" class="error">{{ errors.phone }}</span>
            </div>
          </label>

          <label class="field">
            <span class="field-label">{{ t('users.fields.bank') }}</span>
            <div class="field-control">
              <input
                v-model="form.bank"
                name="bank"
                type="text"
                maxlength="256"
                :disabled="!canEdit"
              />
              <span v-if="errors.bank" class="error">{{ errors.bank }}</span>
            </div>
          </label>

          <label class="field">
            <span class="field-label">{{ t('users.fields.iban') }}</span>
            <div class="field-control">
              <input
                v-model="form.iban"
                name="iban"
                type="text"
                maxlength="34"
                :disabled="!canEdit"
              />
              <span v-if="errors.iban" class="error">{{ errors.iban }}</span>
            </div>
          </label>

          <label class="field">
            <span class="field-label">{{ t('users.fields.swift') }}</span>
            <div class="field-control">
              <input
                v-model="form.swift"
                name="swift"
                type="text"
                maxlength="11"
                :disabled="!canEdit"
              />
              <span v-if="errors.swift" class="error">{{ errors.swift }}</span>
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
  width: min(760px, 100%);
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
  gap: 10px;
  flex-wrap: wrap;
}

h2 {
  margin: 0;
  font-size: 20px;
}

.status {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #6b7280;
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

.section-title {
  margin: 0;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #6b7280;
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
  width: 170px;
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

input:disabled,
textarea:disabled,
select:disabled {
  background: #f1f5f9;
  color: #94a3b8;
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

.section {
  border: 1px solid #e5e7eb;
  background: #f8fafc;
  border-radius: 12px;
  padding: 12px;
  display: grid;
  gap: 12px;
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
  cursor: not-allowed;
}
</style>
