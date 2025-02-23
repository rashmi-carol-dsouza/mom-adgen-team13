<script setup lang="ts">

</script>

<template>
  <header>
    <h1>MoM Team 13</h1>
  </header>
  <main class="main">
    <router-view />
  </main>
  <footer>
    <p>Hacked with 💖 by Team 13 at Measure of Music 2025</p>
  </footer>
</template>

<style scoped>
:host {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}
</style>