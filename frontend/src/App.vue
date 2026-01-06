<script setup>
import { RouterLink, RouterView } from 'vue-router'
import ToastHost from './shared/ToastHost.vue'
import { t } from './shared/i18n'
</script>

<template>
  <div class="app">
    <header class="topbar">
      <div class="brand">
        <span class="logo">{{ t('app.title') }}</span>
        <span class="tag">{{ t('app.tag') }}</span>
      </div>
      <nav class="nav">
        <RouterLink to="/clients">{{ t('app.nav.clients') }}</RouterLink>
      </nav>
    </header>
    <main class="content">
      <RouterView />
    </main>
    <ToastHost />
  </div>
</template>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&display=swap");

:global(body) {
  margin: 0;
  font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
  background: radial-gradient(circle at top left, #f6f4f0 0%, #eef3f9 45%, #f2f6f4 100%);
  color: #1f2933;
}

:global(a) {
  color: inherit;
  text-decoration: none;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 24px;
  border-bottom: 1px solid #d7e0ea;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  letter-spacing: 0.4px;
}

.logo {
  font-size: 18px;
}

.tag {
  font-size: 12px;
  text-transform: uppercase;
  color: #52606d;
  border: 1px solid #d1dae3;
  padding: 2px 6px;
  border-radius: 999px;
}

.nav a {
  font-weight: 600;
  padding-bottom: 4px;
  border-bottom: 2px solid transparent;
}

.nav a.router-link-active {
  border-color: #3b82f6;
}

.content {
  flex: 1;
  padding: 28px 24px 60px;
}

@media (max-width: 640px) {
  .topbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
