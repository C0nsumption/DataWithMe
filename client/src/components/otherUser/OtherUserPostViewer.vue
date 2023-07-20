<!-- OtherUserPostViewer.vue -->
<template>
    <div class="post-viewer-wrapper">
      <h1>Posts</h1>
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="post in posts" :key="post.id">
            <td>{{ post.title }}</td>
            <td>
              <button class="view-button" @click="viewPost(post.id)">View</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="tableHTML" class="modal-backdrop" @click.self="closePost">
        <div class="modal">
          <button @click="closePost">Close</button>
          <div class="table-wrapper" v-html="tableHTML"></div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from 'vue'
import { useStore } from 'vuex'

const { userId } = defineProps(['userId']);
const url = import.meta.env.VITE_API_URL
const store = useStore()

const posts = ref([])
const tableHTML = ref('')

const viewPost = async (postId) => {
  const response = await fetch(`${url}/posts/${postId}`, {
    headers: {
      'Authorization': 'Bearer ' + store.state.token
    }
  })
  const data = await response.json()
  tableHTML.value = data.tableHTML
}

const refreshPostsForOtherUser = async () => {
  const response = await fetch(`${url}/user/posts/${userId}`, {
    headers: {
      'Authorization': 'Bearer ' + store.state.token
    }
  })
  const data = await response.json()
  posts.value = data
}

const closePost = () => {
  tableHTML.value = ''
}

onMounted(refreshPostsForOtherUser)
</script>

  
<style scoped>
.table-wrapper {
  overflow-x: auto;
}

.post-viewer-wrapper{
  border: 1px solid #fff;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background-color: #333;
  padding: 20px;
  max-width: 90vw;
  overflow: auto;
}

button {
  margin: 5px;
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  opacity: 0.8;
}

button:active {
  opacity: 1;
}

.view-button {
  background-color: #0697df; /* Blue */
  color: white;
}

</style>
