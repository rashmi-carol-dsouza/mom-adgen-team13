<script setup>
import { ref } from 'vue';

const emit = defineEmits(['status-change', 'data-loaded']);

const valid = ref(false);
const genre = ref('');
const language = ref('');
const errorMessage = ref('');

const genreRules = [
    v => !!v || 'Genre is required',
];
const languageRules = [
    v => !!v || 'Language is required',
];

const getLocation = () => {
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
                    console.log('Error:', error);
                    reject(new Error('Failed to get location.'));
                }
            );
        } else {
            reject(new Error('Geolocation is not supported by this browser.'));
        }
    });
};

const submit = async () => {
    if (valid.value) {
        emit('status-change', 'loading');
        try {
            const location = await getLocation();
            console.log('Location:', location);
            const data = {
                genre: [genre.value],
                lon: location.lon.toString(),
                lat: location.lat.toString(),
                language: language.value,
            };

            const response = await fetch('https://4argznoorj.execute-api.eu-central-1.amazonaws.com/dev/generated-ads', {
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
            emit('data-loaded', url);
            emit('status-change', 'finished');
        } catch (error) {
            console.error('Error:', error);
            errorMessage.value = 'Failed to generate ad. Please try again.';
            emit('status-change', 'form');
        }
    }
};
</script>

<template>
    <v-form v-model="valid" class="taget-info">
        <v-container>
            <v-col>
                <v-row cols="12" md="4">
                    <v-text-field v-model="genre" :rules="genreRules" :counter="10" label="genre" required></v-text-field>
                </v-row>

                <v-row cols="12" md="4">
                    <v-text-field v-model="language" :rules="languageRules" label="language" required></v-text-field>
                </v-row>
                <v-row cols="12" md="4">
                    <v-btn :disabled="!valid" color="primary" @click="submit">
                        Submit
                    </v-btn>
                </v-row>
                <v-row cols="12" md="4" v-if="errorMessage">
                    <v-alert type="error">{{ errorMessage }}</v-alert> <!-- Display error message -->
                </v-row>
            </v-col>
        </v-container>
    </v-form>
</template>

<style scoped>
.taget-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: start;
    width: 100%;
}
</style>