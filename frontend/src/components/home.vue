<script setup>
import { ref } from 'vue';
import userInput from './userInput.vue';
import player from './player.vue';

const status = ref('form');
let adFromAPI = ref();

const handleStatusChange = (newStatus) => {
  status.value = newStatus;
};

const handleDataLoaded = (fileUrl) => {
  adFromAPI.value = fileUrl;
  status.value = 'finished';
};
</script>

<template>
    <userInput @status-change="handleStatusChange" @data-loaded="handleDataLoaded" />
    <v-progress-circular v-if="status === 'loading'" indeterminate color="primary"></v-progress-circular>
    <player v-if="status === 'finished'" />
</template>

<style scoped>

</style>