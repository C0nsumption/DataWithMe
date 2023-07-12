// store.js
import { createStore } from 'vuex'

export default createStore({
  state: {
    token: null,
    // other state
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      console.log("Token stored in Vuex:", state.token);  // Add this line
    },
    // other mutations
  },
  actions: {
    // actions
  },
  modules: {
    // modules
  }
})
