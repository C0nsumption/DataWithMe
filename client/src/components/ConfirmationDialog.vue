<template>
    <div class="confirmation-modal" v-if="show" @click.self="handleCancel">
      <div class="confirmation-modal-content">
        <span class="close-button" @click="handleCancel">&times;</span>
        <p>{{ message }}</p>
        <div>
          <button @click="handleConfirm">Confirm</button>
          <button @click="handleCancel">Cancel</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  
  const props = defineProps({
    show: Boolean,
    message: String,
    onConfirm: Function,
    onCancel: Function
  })
  
  const handleConfirm = () => {
    props.onConfirm()
  }
  
  const handleCancel = () => {
    props.onCancel()
  }
  </script>
  
  <style scoped>
.confirmation-modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
}

.confirmation-modal-content {
  background-color: #444;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 500px;
}
  
  .close-button {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }
  
  .close-button:hover,
  .close-button:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }
  </style>
  