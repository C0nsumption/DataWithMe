<!-- ProfilePage.vue -->
<template>
  <div>
    <UserProfile v-if="user" :user="user" />
    <PostViewer />
    <PostSubmission v-if="isModalOpen" @close="closeModal" />
    <button @click="openModal">Create New Post</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import PostSubmission from './PostSubmission.vue'
import PostViewer from './PostViewer.vue'
// import UserSearch from '../UserSearch.vue'
import UserProfile from './CurrentUserProfile.vue'

const store = useStore()
const user = ref(null)

onMounted(async () => {
  await store.dispatch('fetchCurrentUser')
  user.value = store.state.currentUser
})

const isModalOpen = ref(false)

const openModal = () => {
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}
</script>
