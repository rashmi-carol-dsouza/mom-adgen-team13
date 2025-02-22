<script>
export default {
    data: () => ({
        valid: false,
        genre: '',
        location: '',
        language: '',
        errorMessage: '', // Add errorMessage property
        genreRules: [
            v => !!v || 'Genre is required',
        ],
        locationRules: [
            v => !!v || 'Location is required',
        ],
        languageRules: [
            v => !!v || 'Language is required',
        ],
    }),
    methods: {
        async submit() {
            if (this.valid) {
                this.$emit('status-change', 'loading');
                const data = {
                    genre: this.genre,
                    location: this.location,
                    language: this.language,
                };

                try {
                    const response = await fetch('http://localhost:8080/generateAd', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data),
                    });

                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }

                    const result = await response.json();
                    console.log('Success:', result);
                    this.$emit('data-loaded', result);
                    this.$emit('status-change', 'finished');
                } catch (error) {
                    console.error('Error:', error);
                    this.errorMessage = 'Failed to generate ad. Please try again.';
                    this.$emit('status-change', 'form');
                }
            }
        },
    },
}
</script>

<template>
    <v-form v-model="valid" class="taget-info">
        <v-container>
            <v-col>
                <v-row cols="12" md="4">
                    <v-text-field v-model="genre" :rules="genreRules" :counter="10" label="genre" required></v-text-field>
                </v-row>

                <v-row cols="12" md="4">
                    <v-text-field v-model="location" :rules="locationRules" :counter="10" label="location" required></v-text-field>
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