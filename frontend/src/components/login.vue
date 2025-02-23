<script setup lang="ts">

const clientId = '8debbbb07e454253bc3da61a7411a163';
const redirectUri = 'http://localhost:5173/callback';
const scope = 'user-read-private user-read-email user-read-playback-state user-read-currently-playing';
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
  <v-btn @click="login">Login with Spotify</v-btn>
</template>

<style scoped>
</style>