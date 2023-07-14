<!-- PostViewer.vue -->
<template>
  <div class="post-viewer-wrapper">
    <div style="display: flex; align-items: center;">
      <h1>Posts</h1>
      <button @click="refreshPosts">Refresh</button>
    </div>
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
            <button class="delete-button" @click="deletePost(post.id)">Delete</button>
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
  <ConfirmationDialog
      :show="showConfirmation"
      message="Are you sure you want to delete this post?"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import ConfirmationDialog from './ConfirmationDialog.vue'

const url = import.meta.env.VITE_API_URL
const store = useStore()

const posts = ref([])
const tableHTML = ref('')
const showConfirmation = ref(false)
let postIdToDelete = null

const viewPost = (postId) => {
  if (store.state.token === null) {
    console.log('No token found. Please log in first.')
    return
  }

  getPost(postId)
}

const deletePost = (postId) => {
  if (store.state.token === null) {
    console.log('No token found. Please log in first.')
    return
  }

  openConfirmation(postId)
}


const getPost = async (postId) => {
  const response = await fetch(`${url}/posts/${postId}`, {
    headers: {
      'Authorization': 'Bearer ' + store.state.token
    }
  })
  const data = await response.json()
  tableHTML.value = data.tableHTML
}

const openConfirmation = (postId) => {
  showConfirmation.value = true
  postIdToDelete = postId
}

const confirmDelete = async () => {
  const response = await fetch(`${url}/posts/${postIdToDelete}`, {
    method: 'DELETE',
    headers: {
      'Authorization': 'Bearer ' + store.state.token
    }
  })
  if (response.ok) {
    refreshPosts()
  }
  showConfirmation.value = false
}

const cancelDelete = () => {
  showConfirmation.value = false
}

const refreshPosts = async () => {
  const response = await fetch(`${url}/posts`, {
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

onMounted(refreshPosts)
</script>

<style>
.table-wrapper table {
  width: 100%;
  border-collapse: collapse;
}

.table-wrapper th,
.table-wrapper td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.table-wrapper th {
  background-color: #023047; 
  color: white;
}

.table-wrapper tr:nth-child(even) {
  background-color: #b6d6e5;
  color: black;

}

.table-wrapper tr:nth-child(odd) {
  background-color: #8ecae6; 
  color: black;

}
</style>



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

.delete-button {
  background-color: #d00e00; /* Red */
  color: white;
}
</style>

