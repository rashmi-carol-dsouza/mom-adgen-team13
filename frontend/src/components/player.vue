<script lang="ts" setup>
import { defineProps } from 'vue';
import { VueSound } from 'vue-sound';

const props = defineProps<{
  src: string;
}>();
</script>

<template>
  <div>
    <VueSound class="player"
      show-download
      title="Ad for your target audience"
      :file="src"
    />
  </div>
</template>

<style scoped>
.player {  
    border-radius: 10px;
    background: linear-gradient(90deg, rgb(163, 0, 76) 0%, rgba(212, 0, 88, 0.849) 55%, rgba(199, 0, 93, 0.993) 100%);
  }
.vue-sound {
  --player-background: linear-gradient(90deg, rgb(163, 0, 136) 0%, rgba(255, 1, 196, 0.952) 55%, rgba(196, 0, 199, 0.993) 100%);
}
</style>