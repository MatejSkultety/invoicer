<script setup>
import { computed, reactive, watch } from 'vue'

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
  main_contact: ''
})

const isEdit = computed(() => Boolean(props.client))

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
}

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      resetForm()
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

function validate() {
  clearErrors()
  let valid = true

  if (!form.name.trim()) {
    errors.name = 'Name is required'
    valid = false
  }

  if (!form.address.trim()) {
    errors.address = 'Address is required'
    valid = false
  }

  if (!form.city.trim()) {
    errors.city = 'City is required'
    valid = false
  }

  if (!form.country.trim()) {
    errors.country = 'Country is required'
    valid = false
  }

  if (!form.main_contact_method) {
    errors.main_contact_method = 'Contact method is required'
    valid = false
  }

  if (!form.main_contact.trim()) {
    errors.main_contact = 'Main contact is required'
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
        <h2>{{ isEdit ? 'Edit client' : 'Create client' }}</h2>
        <button type="button" class="close" @click="close">Close</button>
      </header>

      <form class="form" @submit.prevent="submit">
        <label>
          <span>Name</span>
          <input v-model="form.name" name="name" type="text" autocomplete="name" />
          <span v-if="errors.name" class="error">{{ errors.name }}</span>
        </label>

        <label>
          <span>Address</span>
          <input v-model="form.address" name="address" type="text" autocomplete="street-address" />
          <span v-if="errors.address" class="error">{{ errors.address }}</span>
        </label>

        <label>
          <span>City</span>
          <input v-model="form.city" name="city" type="text" autocomplete="address-level2" />
          <span v-if="errors.city" class="error">{{ errors.city }}</span>
        </label>

        <label>
          <span>Country</span>
          <input v-model="form.country" name="country" type="text" autocomplete="country-name" />
          <span v-if="errors.country" class="error">{{ errors.country }}</span>
        </label>

        <label>
          <span>Main contact method</span>
          <select v-model="form.main_contact_method" name="main_contact_method">
            <option value="email">Email</option>
            <option value="whatsapp">WhatsApp</option>
            <option value="discord">Discord</option>
          </select>
          <span v-if="errors.main_contact_method" class="error">{{ errors.main_contact_method }}</span>
        </label>

        <label>
          <span>Main contact</span>
          <input v-model="form.main_contact" name="main_contact" type="text" />
          <span v-if="errors.main_contact" class="error">{{ errors.main_contact }}</span>
        </label>

        <label>
          <span>Additional contact</span>
          <input v-model="form.additional_contact" name="additional_contact" type="text" />
        </label>

        <label>
          <span>IČO</span>
          <input v-model="form.ico" name="ico" type="text" />
        </label>

        <label>
          <span>DIČ</span>
          <input v-model="form.dic" name="dic" type="text" />
        </label>

        <label>
          <span>Notes</span>
          <textarea v-model="form.notes" name="notes" rows="4"></textarea>
        </label>

        <label class="checkbox">
          <input v-model="form.favourite" name="favourite" type="checkbox" />
          <span>Favourite client</span>
        </label>

        <p v-if="errorMessage" class="error-banner">{{ errorMessage }}</p>

        <div class="actions">
          <button type="button" class="ghost" @click="close">Cancel</button>
          <button type="submit" :disabled="submitting">
            {{ submitting ? 'Saving...' : isEdit ? 'Save changes' : 'Create client' }}
          </button>
        </div>
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
  width: min(520px, 100%);
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.25);
  padding: 22px;
}

header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

h2 {
  margin: 0;
  font-size: 20px;
}

.close {
  border: none;
  background: transparent;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  cursor: pointer;
}

.form {
  display: grid;
  gap: 14px;
}

label {
  display: grid;
  gap: 6px;
  font-size: 14px;
}

input,
textarea,
select {
  border: 1px solid #d2dae3;
  border-radius: 10px;
  padding: 10px 12px;
  font: inherit;
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

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}

.checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
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
</style>
