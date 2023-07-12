<script setup>
import { reactive } from 'vue'
import LoginForm from './components/LoginForm.vue'
import HomePage from './components/HomePage.vue'

const state = reactive({
  isLoggedIn: false
})

const handleLogin = () => {
  console.log('Handling login')
  state.isLoggedIn = true
}
</script>


<template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125"  />

    <div class="wrapper">
    </div>
  </header>

  <main :class="{ 'login-page': !state.isLoggedIn, 'home-page': state.isLoggedIn }">
    <LoginForm v-if="!state.isLoggedIn" @login="handleLogin" />
    <HomePage v-else />
  </main>

  <!-- Debugging -->
  <p>Is logged in: {{ state.isLoggedIn }}</p>
</template>




<!-- existing styles -->

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
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
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
  min-width: 1024px;
  min-height: 95vh;
}

.home-page {
  display: block;
  border: 1px solid #fff;
  min-width: 1024px;
  min-height: 95vh;
}

@media (min-width: 1024px) {
  .logo {
    margin: 0 2rem 0 0;
  }
}
</style>

