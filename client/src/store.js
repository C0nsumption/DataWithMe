// store.js
import { createStore } from 'vuex'

const url = import.meta.env.VITE_API_URL

export default createStore({
  state: {
    token: null,
    // other state
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      console.log("Token stored in Vuex:", state.token);
    },
    clearToken(state) {
      state.token = null;
    },
    // other mutations
  },
  actions: {
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
    // other actions
  },
  modules: {
    // modules
  }
})
