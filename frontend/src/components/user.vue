<script setup lang="ts">
import { ref, onMounted } from 'vue';

const isLoggedIn = (): boolean => {
  return !!localStorage.getItem('access_token');
}

if (!isLoggedIn()) {
  window.location.href = '/';
}

interface CurrentlyPlaying {
  item: {
    name: string;
    artists: { name: string }[];
  };
}

const currentlyPlaying = ref<CurrentlyPlaying | null>(null);

const fetchCurrentlyPlaying = async () => {
  const accessToken = localStorage.getItem('access_token');
  if (!accessToken) {
    return;
  }

  const response = await fetch('https://api.spotify.com/v1/me/player/currently-playing', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    }
  });

  if (response.ok) {
    currentlyPlaying.value = await response.json();
  } else {
    console.error('Failed to fetch currently playing track:', response.statusText);
  }
}

onMounted(() => {
  fetchCurrentlyPlaying();
});
</script>

<template>
  <div v-if="currentlyPlaying">
    <h2>Currently Playing</h2>
    <p>{{ currentlyPlaying.item.name }} by {{ currentlyPlaying.item.artists[0].name }}</p>
  </div>
  <div v-else>
    <p>No track is currently playing.</p>
  </div>
</template>

<style scoped>
</style>