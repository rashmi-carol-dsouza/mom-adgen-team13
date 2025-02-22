<script>
export default {
    data: () => ({
        valid: false,
        genre: '',
        location: '',
        language: '',
    }),
}
</script>

<template>
    <v-form v-model="valid" class="taget-info">
        <v-container>
            <v-col>
                <v-row cols="12" md="4">
                    <v-text-field v-model="genre" :counter="10" label="genre" required></v-text-field>
                </v-row>

                <v-row cols="12" md="4">
                    <v-text-field v-model="location" :counter="10" label="location" required></v-text-field>
                </v-row>

                <v-row cols="12" md="4">
                    <v-text-field v-model="language" :rules="language" label="language" required></v-text-field>
                </v-row>
                <v-row cols="12" md="4">
                    <v-btn :disabled="!valid" color="primary" @click="submit">
                        Submit
                    </v-btn>
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
    height: 100vh;
    width: 100%;
}
</style>