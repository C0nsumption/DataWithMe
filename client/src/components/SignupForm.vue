<!-- SignupForm.vue -->
<template>
  <div class="form-container">
    <h2>Sign Up</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="signupUsername">Username:</label>
        <input type="text" id="signupUsername" v-model="signupUsername" required>
      </div>
      <div>
        <label for="signupPassword">Password:</label>
        <input type="password" id="signupPassword" v-model="signupPassword" required>
      </div>
      <div>
        <label for="signupName">Name:</label>
        <input type="text" id="signupName" v-model="signupName" required>
      </div>
      <button type="submit" class="general-button">Sign Up</button>
    </form>
    <span>
      <p>Already have an account?</p>
      <a @click="$emit('changeForm', 'login')">Back to Login</a>
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


const signupUsername = ref('')
const signupPassword = ref('')
const signupName = ref('')  // New field

const message = ref('')

// Define the 'signup' and 'changeForm' events that this component will emit
const emit = defineEmits(['signup', 'changeForm'])


const submitForm = async () => {
  const requestUrl = `${url}/signup`
  const response = await fetch(requestUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: signupUsername.value,
      password: signupPassword.value,
      name: signupName.value,  // Include name in the request
    }),
  })

  const data = await response.json()
  message.value = data.message

  console.log('Response status:', response.status);
  console.log('Response data:', data);

  if (response.status === 201) {
    store.commit('setToken', data.token);  // Save the token in the store
    emit('signup', signupUsername.value)
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
