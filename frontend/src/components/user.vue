<script setup lang="ts">
import { ref, onMounted } from 'vue';
import player from './player.vue';

const emit = defineEmits(['status-change', 'data-loaded']);

const isLoggedIn = (): boolean => {
  return !!localStorage.getItem('access_token');
}

if (!isLoggedIn()) {
  window.location.href = '/';
}

interface CurrentlyPlaying {
  item: {
    name: string;
    artists: { name: string; id: string }[];
    album: {
      images: { url: string }[];
    };
  };
}

interface Artist {
  genres: string[];
}

const currentlyPlaying = ref<CurrentlyPlaying | null>(null);
const adFromAPI = ref<string | null>(null);
const artistGenres = ref<string[]>([]);

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
    if (currentlyPlaying.value && currentlyPlaying.value.item.artists.length > 0) {
      const artistId = currentlyPlaying.value.item.artists[0].id;
      await fetchArtistGenres(artistId);
    }
  } else {
    console.error('Failed to fetch currently playing track:', response.statusText);
  }
}

const fetchArtistGenres = async (artistId: string) => {
  const accessToken = localStorage.getItem('access_token');
  if (!accessToken) {
    return;
  }

  const response = await fetch(`https://api.spotify.com/v1/artists/${artistId}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    }
  });

  if (response.ok) {
    const artist: Artist = await response.json();
    artistGenres.value = artist.genres;
  } else {
    console.error('Failed to fetch artist genres:', response.statusText);
  }
}

const errorMessage = ref('');

const getLocation = (): Promise<{ lon: number, lat: number }> => {
  return new Promise((resolve, reject) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        position => {
          resolve({
            lon: position.coords.longitude,
            lat: position.coords.latitude
          });
        },
        error => {
          switch (error.code) {
            case error.PERMISSION_DENIED:
              reject(new Error('User denied the request for Geolocation.'));
              break;
            case error.POSITION_UNAVAILABLE:
              reject(new Error('Location information is unavailable.'));
              break;
            case error.TIMEOUT:
              reject(new Error('The request to get user location timed out.'));
              break;
            default:
              reject(new Error('An unknown error occurred.'));
              break;
          }
        }
      );
    } else {
      reject(new Error('Geolocation is not supported by this browser.'));
    }
  });
};

const submit = async () => {
  emit('status-change', 'loading');
  try {
    const location = await getLocation();
    const data = {
      genre: artistGenres.value,
      lon: location.lon.toString(),
      lat: location.lat.toString(),
      language: 'English',
    };

    const response = await fetch('https://wdueh6plo9.execute-api.eu-central-1.amazonaws.com/dev/generated-ads', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'audio/mpeg',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    console.log('Success:', url);
    adFromAPI.value = url;
    emit('data-loaded', url);
    emit('status-change', 'finished');
  } catch (error) {
    console.error('Error:', error);
    errorMessage.value = 'Failed to generate ad. Please try again.';
    emit('status-change', 'form');
  }
}

onMounted(() => {
  fetchCurrentlyPlaying();
});
</script>

<template>
  <div v-if="currentlyPlaying" class="container">
    <h2>User location: Hamburg, Germany</h2>
    <p>User is currently listening to</p>
    <img :src="currentlyPlaying.item.album.images[0].url" alt="Album cover" class="album-cover" />
    <h2>{{ currentlyPlaying.item.name }}</h2>
    <p>by <b>{{ currentlyPlaying.item.artists[0].name }}</b></p>
    <p>✅There are relevent events in the users area!</p>
    <v-btn class="btn" @click="submit">Generate Ad</v-btn>
    <v-alert v-if="errorMessage" type="error">{{ errorMessage }}</v-alert>
    <player v-if="adFromAPI"/>
  </div>
  <div v-else>
    <p>No track is currently playing.</p>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: start;
  gap: 1rem;
  margin-top: 10%;

  .btn {
    background: linear-gradient(90deg, rgb(163, 0, 76) 0%, rgba(212, 0, 88, 0.849) 55%, rgba(199, 0, 93, 0.993) 100%);
    color: white;
    border: solid 2px hotpink;
    height: 50px;
    width: 180px;
}
}

.album-cover {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 10px;
}
</style>