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
    <UserSearch v-if="state.isLoggedIn" @userClicked="loadUserProfile" />
    <ProfilePage v-if="state.isLoggedIn" />
    <OtherProfilePage v-if="selectedUser" :user="selectedUser" @close-modal="closeOtherProfileModal"/>

  </main>

</template>

<script setup>
import { reactive, ref } from 'vue'
import { useStore } from 'vuex'
import LoginForm from './components/LoginForm.vue'
import SignupForm from './components/SignupForm.vue'
import ProfilePage from './components/currentUser/ProfilePage.vue'
import UserSearch from './components/UserSearch.vue'
import OtherProfilePage from './components/otherUser/OtherProfilePage.vue'
import LogOut from './components/LogOut.vue'

const formType = ref('login')
const store = useStore()
const selectedUser = ref(null)

const loadUserProfile = async (user) => {
    selectedUser.value = await store.dispatch('fetchFullUserProfile', user.username)
}

const changeForm = (newFormType) => {
  formType.value = newFormType
}

const state = reactive({
  isLoggedIn: false,
  username: null  // add this line
})

const handleLogin = (username) => {
  console.log('Handling login')
  state.isLoggedIn = true
  state.username = username
  store.commit('setCurrentUser', username);  // use mutation to set currentUser
}



const handleLogout = () => {
  state.isLoggedIn = false
  state.username = null
}

const closeOtherProfileModal = () => {
    selectedUser.value = null;
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

