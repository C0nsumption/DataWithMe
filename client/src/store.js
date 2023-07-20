// store.js
import { createStore } from 'vuex'

const url = import.meta.env.VITE_API_URL

export default createStore({
  state: {
    token: null,
    currentUser: null,
    selectedUserProfile: null  // new state property
    // other state
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      console.log("Token stored in Vuex:", state.token);
    },
    setCurrentUser(state, user) {  // add this mutation
      state.currentUser = user;
    },
    clearToken(state) {
      state.token = null;
    },
    setSelectedUserProfile(state, user) {  // new mutation
      state.selectedUserProfile = user;
    },
    // other mutations
  },
  actions: {
    async fetchCurrentUser({ commit, state }) {  // add this action
      const response = await fetch(`${url}/user/${state.currentUser}`, {
        headers: { 'Authorization': `Bearer ${state.token}` }
      })
    
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    
      const user = await response.json()
      commit('setCurrentUser', user)  // here user should be user object, not username
    },
    
    async searchUser({ state }, username) {
      try {
        const response = await fetch(`${url}/search_user/${username}`, {
          headers: { 'Authorization': `Bearer ${state.token}` }
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json()
        console.log(data);  // log the data
        return data
      } catch (error) {
        console.error('Error reading response body:', error);
      }
    },
    async fetchFullUserProfile({ commit, state }, username) {
      try {
          const response = await fetch(`${url}/user/${username}`, {
              headers: { 'Authorization': `Bearer ${state.token}` }
          });

          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }

          const user = await response.json();
          commit('setSelectedUserProfile', user);  // use the new mutation
          return user;
      } catch (error) {
          console.error('Error fetching full user profile:', error);
      }
  }
  
    // other actions
  },
  modules: {
    // modules
  }
})
