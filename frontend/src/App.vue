<script setup lang="ts">
import { ref } from 'vue';
import userInput from './components/userInput.vue';
import player from './components/player.vue';

const status = ref('form');
let adFromAPI = ref(null);

const handleStatusChange = (newStatus: string) => {
  status.value = newStatus;
};

const handleDataLoaded = (data) => {
  adFromAPI.value = data;
  status.value = 'finished';
};
</script>

<template>
  <header>
    <h1>MoM Team 13</h1>
  </header>
  <main class="main">
    <userInput @status-change="handleStatusChange" @data-loaded="handleDataLoaded" />
    <v-progress-circular v-if="status === 'loading'" indeterminate color="primary"></v-progress-circular>
    <player v-if="status === 'finished'" />
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