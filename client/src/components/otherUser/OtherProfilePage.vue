<!-- OtherProfilePage.vue -->
<template>
    <div class="other-profile-modal" @click.self="closeModal">
      <div class="other-profile-modal-content">
        <span class="close-button" @click="closeModal">&times;</span>
        <OtherUserProfile :user="user" />
        <!-- Additional components related to the other user's profile can be added here -->
      </div>
    </div>
</template>
  
<script setup>
import { computed, defineEmits } from 'vue'
import { useStore } from 'vuex'
import OtherUserProfile from './OtherUserProfile.vue'

const store = useStore();

// Use the user from the store
const user = computed(() => store.state.selectedUserProfile);

const emit = defineEmits(["close-modal"]);

const closeModal = () => {
    emit('close-modal');
}
</script>

  
  
  <style scoped>
  .other-profile-modal {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    z-index: 1000; /* Ensures it's above other content */
  }
  
  .other-profile-modal-content {
    background-color: #333;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
    max-width: 500px;
    position: relative;
  }
  
  .close-button {
    color: #aaa;
    position: absolute;
    right: 10px;
    top: 10px;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
  }
  
  .close-button:hover,
  .close-button:focus {
    color: black;
  }
  </style>
  
