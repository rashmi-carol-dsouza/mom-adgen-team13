<script setup lang="ts">
import { ref, onMounted } from 'vue';

const getToken = async (code: string) => {
  const codeVerifier = localStorage.getItem('code_verifier');

  const url = "https://accounts.spotify.com/api/token";
  const payload = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      client_id: '8debbbb07e454253bc3da61a7411a163',
      grant_type: 'authorization_code',
      code,
      redirect_uri: 'https://team13.surge.sh/callback',
      code_verifier: codeVerifier || '',
    }).toString(),
  }

  const body = await fetch(url, payload);
  const response = await body.json();

  localStorage.setItem('access_token', response.access_token);
}

onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get('code');
  if (code) {
    getToken(code).then(() => {
      window.location.href = '/user';
    });
  }
});
</script>

<template>
  <div>
    <h1>Callback</h1>
  </div>
</template>

<style scoped>
</style>