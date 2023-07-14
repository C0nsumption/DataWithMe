<!-- UserSearch.vue -->
<template>
    <div class="user-search">
      <input 
        type="text" 
        v-model="username" 
        placeholder="Search users" 
        @keyup="invokeSearch"
        class="search-input"
      />
    
      <div class="user-list" v-if="users.length">
        <div 
          class="user" 
          v-for="user in users" 
          :key="user.id" 
          @click="handleClick(user)"
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
        }
      }
  
      const handleClick = (user) => {
        console.log(user)
      }
  
      return {
        username,
        users,
        invokeSearch,
        handleClick
      }
    }
}
</script>

<style scoped>
.user-search {
  width: 400px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
  color: #333;
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
  list-style-type: none;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.user {
  padding: 10px;
  border-bottom: 1px solid #ccc;
  cursor: pointer;
}

.user:hover {
  background-color: #f9f9f9;
}
</style>
