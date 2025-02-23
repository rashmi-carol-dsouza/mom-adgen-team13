<script setup lang="ts">
import { ref } from 'vue';

const clientId = '8debbbb07e454253bc3da61a7411a163';
const redirectUri = 'https://team13.surge.sh/callback';
const scope = 'user-read-private user-read-email';
let authUrl: string = '';

const generateRandomString = (length: number): string => {
  const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  const values = crypto.getRandomValues(new Uint8Array(length));
  return values.reduce((acc, x) => acc + possible[x % possible.length], "");
}

const codeVerifier = generateRandomString(64);

const sha256 = async (plain: string): Promise<ArrayBuffer> => {
  const encoder = new TextEncoder();
  const data = encoder.encode(plain);
  return window.crypto.subtle.digest('SHA-256', data);
}

const base64encode = (input: ArrayBuffer): string => {
  return btoa(String.fromCharCode(...new Uint8Array(input)))
    .replace(/=/g, '')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
}

const setupAuthUrl = async () => {
  const hashed = await sha256(codeVerifier);
  const codeChallenge = base64encode(hashed);

  window.localStorage.setItem('code_verifier', codeVerifier);

  const params = {
    response_type: 'code',
    client_id: clientId,
    scope,
    code_challenge_method: 'S256',
    code_challenge: codeChallenge,
    redirect_uri: redirectUri,
  }

  const url = new URL("https://accounts.spotify.com/authorize");
  url.search = new URLSearchParams(params).toString();
  authUrl = url.toString();
}

setupAuthUrl();

const login = () => {
  window.location.href = authUrl;
}
</script>

<template>
  <header>
    <h1>MoM Team 13</h1>
  </header>
  <main class="main">
    <v-btn @click="login">Login with Spotify</v-btn>
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