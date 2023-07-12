<template>
  <div class="post-submission-wrapper">
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
        <input type="file" id="file" ref="file" @change="handleFileUpload($event)"/>
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'

const url = import.meta.env.VITE_API_URL
const store = useStore()

const title = ref('')
const description = ref('')
const file = ref('')
const message = ref('')

function handleFileUpload(event) {
  file.value = event.target.files[0]
}

async function submitPost() {
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
  message.value = data.message
}
</script>

<style scoped>
.post-submission-wrapper{
  border: 1px solid #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
