<script setup>
import { reactive } from 'vue'
import LoginForm from './components/LoginForm.vue'
import ProfilePage from './components/ProfilePage.vue'

const state = reactive({
  isLoggedIn: false,
  username: null  // add this line
})

const handleLogin = (username) => {  // receive the username here
  console.log('Handling login')
  state.isLoggedIn = true
  state.username = username  // and store it in the state
}
</script>


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
  </header>

  <main :class="{ 'login-page': !state.isLoggedIn, 'profile-page': state.isLoggedIn }">
    <LoginForm v-if="!state.isLoggedIn" @login="handleLogin" />
    <ProfilePage v-else />
  </main>

</template>



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

