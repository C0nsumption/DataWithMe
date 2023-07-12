<template>
    <div>
      <h1>Home</h1>
      <p>One hell of a homepage, isn't it?</p>
      <PostSubmission />
      <PostViewer />
    </div>
  </template>
  
  <script>
  import PostSubmission from './PostSubmission.vue'
  import PostViewer from './PostViewer.vue'

  
  export default {
    components: {
      PostSubmission,
      PostViewer
    }
  }
  </script>
  