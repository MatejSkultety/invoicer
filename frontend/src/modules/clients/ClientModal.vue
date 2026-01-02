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
  email: '',
  notes: ''
})

const errors = reactive({
  name: '',
  address: '',
  email: '',
  notes: ''
})

const isEdit = computed(() => Boolean(props.client))

const emailPattern = /^[^@\s]+@[^@\s]+\.[^@\s]+$/

function resetForm() {
  const source = props.client
  form.name = source ? source.name : ''
  form.address = source ? source.address : ''
  form.email = source ? source.email : ''
  form.notes = source ? source.notes : ''
  clearErrors()
}

function clearErrors() {
  errors.name = ''
  errors.address = ''
  errors.email = ''
  errors.notes = ''
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

  if (!form.email.trim()) {
    errors.email = 'Email is required'
    valid = false
  } else if (!emailPattern.test(form.email.trim())) {
    errors.email = 'Enter a valid email'
    valid = false
  }

  if (!form.notes.trim()) {
    errors.notes = 'Notes are required'
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
    email: form.email.trim(),
    notes: form.notes.trim()
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
          <input v-model="form.name" type="text" autocomplete="name" />
          <span v-if="errors.name" class="error">{{ errors.name }}</span>
        </label>

        <label>
          <span>Address</span>
          <input v-model="form.address" type="text" autocomplete="street-address" />
          <span v-if="errors.address" class="error">{{ errors.address }}</span>
        </label>

        <label>
          <span>Email</span>
          <input v-model="form.email" type="email" autocomplete="email" />
          <span v-if="errors.email" class="error">{{ errors.email }}</span>
        </label>

        <label>
          <span>Notes</span>
          <textarea v-model="form.notes" rows="4"></textarea>
          <span v-if="errors.notes" class="error">{{ errors.notes }}</span>
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
textarea {
  border: 1px solid #d2dae3;
  border-radius: 10px;
  padding: 10px 12px;
  font: inherit;
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
