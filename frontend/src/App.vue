<script setup lang="ts">
  import userInput from './components/userInput.vue'
</script>

<template>
  <header>
    <h1>MoM Team 13</h1>
  </header>
  <main>
    <userInput />
  </main>
</template>

<style scoped>
:host {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}
</style>
