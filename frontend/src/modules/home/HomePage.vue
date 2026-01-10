<script setup>
import { t } from '../../shared/i18n'
</script>

<template>
  <section class="page">
    <header class="header">
      <div>
        <p class="eyebrow">{{ t('home.page.subtitle') }}</p>
        <h1>{{ t('home.page.title') }}</h1>
      </div>
    </header>
    <div class="card">
      <p>{{ t('home.page.body') }}</p>
    </div>
  </section>
</template>

<style scoped>
.page {
  max-width: 960px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.header {
  display: flex;
  align-items: flex-end;
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

.card {
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  border: 1px solid #e1e8f0;
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.08);
  color: #1f2933;
}

@media (max-width: 640px) {
  .header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
