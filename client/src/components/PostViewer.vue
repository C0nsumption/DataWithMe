<template>
    <div class="post-viewer-wrapper">
      <div style="display: flex; align-items: center;">
        <h1>Posts</h1>
        <button @click="refreshPosts">Refresh</button>
      </div>
      <ul>
        <li v-for="post in posts" :key="post.id">
          <a @click="getPost(post.id)">{{ post.title }}</a>
        </li>
      </ul>
      <div v-if="tableHTML">
        <button @click="closePost">Close</button>
        <div class="table-wrapper" v-html="tableHTML"></div>
      </div>
    </div>
</template>

<script setup>


import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'


const posts = ref([])
const tableHTML = ref('')
const store = useStore()


const getPost = async (postId) => {
    console.log(store)
    console.log('Fetching post with token:', store.state.token)
    const response = await fetch(`http://127.0.0.1:5000/posts/${postId}`, {
      headers: {
        'Authorization': 'Bearer ' + store.state.token
      }
    })
    const data = await response.json()
    console.log('Response from getPost:', data)
    tableHTML.value = data.tableHTML
}


const refreshPosts = async () => {
    console.log(store)
    console.log('Refreshing posts with token:', store.state.token)
    const response = await fetch(`http://127.0.0.1:5000/posts`, {
      headers: {
        'Authorization': 'Bearer ' + store.state.token
      }
    })
    const data = await response.json()
    console.log('Response from refreshPosts:', data)
    posts.value = data
}

const closePost = () => {
    tableHTML.value = ''
}

onMounted(refreshPosts)
</script>


<style scoped>
.table-wrapper {
  overflow-x: auto;
}

.post-viewer-wrapper{
    border: 1px solid #fff;
}
</style>
