<!-- CurrentUserProfile.vue -->
<template>
    <div class="profile-container">
      <img class="profile-photo" :src="fullImageUrl" alt="Profile photo">
      <div class="profile-info">
        <h1>{{ user.name }}</h1>
        <h2>Bio:</h2>
        <p>{{ user.bio ? user.bio : 'User has not filled in bio' }}</p>
      </div>
    </div>
</template>
  
<script setup>
import { computed } from 'vue'

const props = defineProps({
  user: Object
})

// Get base URL from environment variables
const baseUrl = import.meta.env.VITE_API_URL

// Compute full image URL
const fullImageUrl = computed(() => `${baseUrl}${props.user.profile_photo}`)
</script>

<style scoped>
.profile-container {
    display: flex;
    align-items: start;
    gap: 20px;
}

.profile-photo {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 50%;
}

.profile-info {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
</style>
