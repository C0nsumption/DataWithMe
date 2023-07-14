<template>
  <div>
      <h1>User Profile</h1>
      <p>One hell of a homepage, isn't it?</p>
      <PostViewer />
      <PostSubmission v-if="isModalOpen" @close="closeModal" />

      <button @click="openModal">Create New Post</button>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import PostSubmission from './PostSubmission.vue'
import PostViewer from './PostViewer.vue'

const isModalOpen = ref(false)

const openModal = () => {
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}
</script>

