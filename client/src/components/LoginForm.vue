<!-- LoginForm.vue -->
<template>
  <div class="form-container">
    <h2>Login</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit" class="general-button">Login</button>
    </form>
    <span>
      <p>Don't have an account?</p>
      <a @click="$emit('changeForm', 'signup')">Sign up here</a>
    </span>
    <span>
      <p v-if="message">{{ message }}</p>
    </span>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'  // Import useStore

const url = import.meta.env.VITE_API_URL

const store = useStore()  // Create a store instance

const username = ref('')
const password = ref('')

const message = ref('')

// Define the 'login' event that this component will emit
const emit = defineEmits(['login', 'changeForm'])

const submitForm = async () => {
  console.log(url)
  const requestUrl = `${url}/login`
  console.log(requestUrl)
  const response = await fetch(requestUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: username.value,
      password: password.value,
    }),
  })

  const data = await response.json()
  message.value = data.message

  console.log('Response status:', response.status);
  console.log('Response data:', data);
  if (response.status === 200) {
    store.commit('setToken', data.token);  // Save the token in the store
    emit('login', username.value)  // Emit the 'login' event with the username
  }
}
</script>



<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 200px;
}

.general-button {
  margin: 10px 0 0 0;
}

span {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
