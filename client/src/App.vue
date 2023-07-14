<!-- App.vue -->

<template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125"  />

    <div class="wrapper">
    </div>

    <!-- Debugging -->
    <p v-if="state.isLoggedIn"> 
      Log In Profile: <span class="loggedIn">{{ state.username }}</span>
    </p>
    <p>
      Log In Status: <span :class="state.isLoggedIn ? 'loggedIn' : 'loggedOut'">{{ state.isLoggedIn }}</span>
    </p>
    <LogOut v-if="state.isLoggedIn" @logout="handleLogout" />

  </header>

  <main :class="{ 'login-page': !state.isLoggedIn, 'profile-page': state.isLoggedIn }">
    <LoginForm v-if="!state.isLoggedIn && formType === 'login'" @login="handleLogin" @changeForm="changeForm" />
    <SignupForm v-if="!state.isLoggedIn && formType === 'signup'" @signup="handleLogin" @changeForm="changeForm" />
    <ProfilePage v-if="state.isLoggedIn" />
  </main>

</template>

<script setup>
import { reactive, ref } from 'vue'
import LoginForm from './components/LoginForm.vue'
import SignupForm from './components/SignupForm.vue'
import ProfilePage from './components/ProfilePage.vue'
import LogOut from './components/LogOut.vue'

const formType = ref('login')

const changeForm = (newFormType) => {
  formType.value = newFormType
}

const state = reactive({
  isLoggedIn: false,
  username: null  // add this line
})

const handleLogin = (username) => {  // receive the username here
  console.log('Handling login')
  state.isLoggedIn = true
  state.username = username  // and store it in the state
}

const handleLogout = () => {
  state.isLoggedIn = false
  state.username = null
}
</script>


<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

header {
    display: flex;
    flex-direction: column;
    place-items: center;
    justify-content: center;
    /* padding-right: calc(var(--section-gap) / 2); */
  }

header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #fff;
  min-width: 80vw;
  min-height: 95vh;
}

.profile-page {
  display: block;
  border: 1px solid #fff;
  min-width: 80vw;
  min-height: 95vh;
}

@media (min-width: 1024px) {
.logo {
    /* margin: 0 2rem 0; */
  }
}

.loggedIn {
  color: hsla(160, 100%, 37%, 1); /* Green */
}

.loggedOut {
  color: hsla(0, 100%, 50%, 1); /* Red or Orange */
}
</style>

