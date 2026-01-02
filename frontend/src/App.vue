<script setup>
import { onMounted, ref } from 'vue'

const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const status = ref('checking...')

onMounted(async () => {
  try {
    const response = await fetch(`${apiBase}/health`)
    if (!response.ok) {
      throw new Error('Health check failed')
    }
    const data = await response.json()
    status.value = data.status || 'unknown'
  } catch (error) {
    status.value = 'unreachable'
  }
})
</script>

<template>
  <div class="page">
    <header class="hero">
      <p class="eyebrow">Local-first invoicing</p>
      <h1>Invoice App (dev)</h1>
    </header>
    <section class="card">
      <p class="label">Backend status</p>
      <p class="status">{{ status }}</p>
    </section>
  </div>
</template>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600&display=swap");

:global(body) {
  margin: 0;
  font-family: "Space Grotesk", "Trebuchet MS", sans-serif;
  background: linear-gradient(140deg, #f7f4ef 0%, #e3edf7 45%, #f1f7f5 100%);
  color: #1f2933;
}

.page {
  max-width: 760px;
  margin: 0 auto;
  padding: 56px 20px 80px;
}

.hero {
  margin-bottom: 28px;
}

.eyebrow {
  margin: 0 0 10px;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 12px;
  color: #52606d;
}

h1 {
  margin: 0;
  font-size: 36px;
  letter-spacing: 0.2px;
}

.card {
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #dbe4ee;
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
  padding: 20px 24px;
}

.label {
  margin: 0 0 6px;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1.6px;
  color: #6b7280;
}

.status {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}
</style>
