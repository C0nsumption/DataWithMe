<!-- PostSubmission.vue -->
<template>
  <div class="modal" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <span class="close-button" @click="$emit('close')">&times;</span>
      <h1>Post Submission</h1>
      <form @submit.prevent="submitPost">
        <div>
          <label>Title:</label>
          <input type="text" v-model.trim="title" required />
        </div>
        <div>
          <label>Description:</label>
          <input type="text" v-model.trim="description" required />
        </div>
        <div>
          <label>File:</label>
          <input type="file" id="file" ref="file" @change="handleFileUpload" />
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'

const url = import.meta.env.VITE_API_URL
const store = useStore()

const title = ref('')
const description = ref('')
const file = ref(null)

const handleFileUpload = (event) => {
  file.value = event.target.files[0]
}

const submitPost = async () => {
  let formData = new FormData()
  formData.append('title', title.value)
  formData.append('description', description.value)
  formData.append('file', file.value)

  const response = await fetch(`${url}/post`, {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + store.state.token
    },
    body: formData
  })

  const data = await response.json()
  console.log(data.message)
}
</script>

<style scoped>
.modal {
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

.modal-content {
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
