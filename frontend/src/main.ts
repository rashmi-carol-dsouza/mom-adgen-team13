import './assets/main.css'

import { createApp } from 'vue'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createRouter, createWebHistory } from 'vue-router';
import Home from './components/home.vue';
import Callback from './components/callback.vue';
import User from './components/user.vue';
import App from './App.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/callback', component: Callback },
  { path: '/user', component: User },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;


const vuetify = createVuetify({
  components,
  directives,
})

createApp(App).use(vuetify).use(router).mount('#app')
