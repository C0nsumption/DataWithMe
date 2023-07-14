<template>
    <div class="user-search">
      <input 
        type="text" 
        v-model="username" 
        placeholder="Search users" 
        @keyup="invokeSearch"
        @blur="invokeBlur"
        class="search-input"
      />
    
      <div class="user-list" v-if="users.length" @click.self="closeSearch">
        <div 
          class="user" 
          v-for="user in users" 
          :key="user.id" 
          @click.stop="handleClick(user)"
        >
          {{ user.username }}
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue'
  import { useStore } from 'vuex'
    
  export default {
    name: 'UserSearch',
    setup() {
      const store = useStore()
      const username = ref('')
      const users = ref([])
    
      const invokeSearch = async () => {
        if (username.value) {
          users.value = await store.dispatch('searchUser', username.value)
        } else {
          users.value = [] // clear users when input is empty
        }
      }
  
      const invokeBlur = () => {
        setTimeout(() => { users.value = [] }, 200) // clear users when focus is lost, with delay for click event
      }
    
      const handleClick = (user) => {
        console.log(user)
      }
      
      const closeSearch = () => {
        users.value = [] // clear users when clicked outside
      }
    
      return {
        username,
        users,
        invokeSearch,
        handleClick,
        invokeBlur,
        closeSearch
      }
    }
  }
  </script>

<style scoped>
.user-search {
  width: 400px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
  color: #aaa;
  position: relative; /* Add this */
}

.search-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.user-list {
  padding: 0;
  background-color: #222;
  list-style-type: none;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  position: absolute; /* Add this */
  width: 100%; /* Add this */
  z-index: 1; /* Add this */
}

.user {
  padding: 10px;
  border-bottom: 1px solid #aaa;
  cursor: pointer;
}

.user:hover {
  background-color: #f9f9f9;
  color: #222;
}
</style>

