<template>
  <div>
    <div v-if="view === 'login'" class="form-container">
      <h2>Login</h2>
      <form @submit.prevent="submitForm('login')">
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
        <a @click="view = 'signup'">Sign up here</a>
      </span>
    </div>

    <div v-else class="form-container">
      <h2>Sign Up</h2>
      <form @submit.prevent="submitForm('signup')">
        <div>
          <label for="signupUsername">Username:</label>
          <input type="text" id="signupUsername" v-model="signupUsername" required>
        </div>
        <div>
          <label for="signupPassword">Password:</label>
          <input type="password" id="signupPassword" v-model="signupPassword" required>
        </div>
        <button type="submit" class="general-button">Sign Up</button>
      </form>
      <span>
        <p>Already have an account?</p>
        <a @click="view = 'login'">Back to Login</a>
      </span>
    </div>
    <span>
    <p v-if="message">{{ message }}</p>
    </span>
  </div>
</template>

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

<script setup>
import { ref, defineEmits } from 'vue'
import { useStore } from 'vuex'  // Import useStore

const url = import.meta.env.VITE_API_URL


const store = useStore()  // Create a store instance

const username = ref('')
const password = ref('')
const signupUsername = ref('')
const signupPassword = ref('')
const message = ref('')
const view = ref('login')

// Define the 'login' event that this component will emit
const emit = defineEmits(['login'])

const submitForm = async (formType) => {
  console.log(url)
  let requestUrl = `${url}/login`
  console.log(requestUrl)
  let user = username.value
  let pass = password.value

  if (formType === 'signup') {
    requestUrl = `${url}/signup`
    console.log(requestUrl)

    user = signupUsername.value
    pass = signupPassword.value
  }

  const response = await fetch(requestUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: user,
      password: pass,
    }),
  })

  const data = await response.json()
  message.value = data.message

  console.log('Response status:', response.status);
  console.log('Response data:', data);
  if (response.status === 200) {
    store.commit('setToken', data.token);  // Save the token in the store
    emit('login')  // Emit the 'login' event 
  }
}
</script>

