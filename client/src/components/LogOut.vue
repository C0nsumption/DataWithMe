<!-- LogOut.vue -->
<template>
    <div>
      <button @click="showConfirmation = true">Log Out</button>
      <ConfirmationDialog
        :show="showConfirmation"
        message="Are you sure you want to log out?"
        @confirm="handleConfirm"
        @cancel="handleCancel"
      />
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useStore } from 'vuex'
  import ConfirmationDialog from './ConfirmationDialog.vue'
  
  const store = useStore()
  const showConfirmation = ref(false)
  
  const handleConfirm = () => {
    store.commit('setToken', null)
    emit('logout')
    showConfirmation.value = false
  }
  
  const handleCancel = () => {
    showConfirmation.value = false
  }
  
  const emit = defineEmits(['logout'])
  </script>
  