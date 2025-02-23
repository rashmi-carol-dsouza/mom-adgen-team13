<script setup lang="ts">
</script>

<template>
  <div class="container">
    <header>
      <h1><b>Spotlight</b></h1>
    </header>
    <main>
      <router-view />
    </main>
    <footer>
      <p>Hacked with 💖 by Team 13 at Measure of Music 2025</p>
    </footer>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header {
  text-align: center;
  padding: 1rem;
  margin-top: 10%;
}

main {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: start;
  width: 100%;
}

footer {
  text-align: center;
  padding: 1rem;
  width: 100%;
  margin-bottom: 15%;
}

.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: radial-gradient(rgba(255, 192, 203, 0.3) 10%, transparent 10%);
    background-size: 40px 40px; /* Adjust dot spacing */
    pointer-events: none;
}

</style>