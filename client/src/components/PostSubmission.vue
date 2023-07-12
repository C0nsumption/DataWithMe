<template>
  <div class="post-submission-wrapper">
    <h1>Post Submission</h1>
    <form @submit.prevent="submitPost">
      <div>
        <label>Title:</label>
        <input type="text" v-model="title" />
      </div>
      <div>
        <label>Description:</label>
        <input type="text" v-model="description" />
      </div>
      <div>
        <label>File:</label>
        <input type="file" id="file" ref="file" v-on:change="handleFileUpload"/>
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<style scoped>
.post-submission-wrapper{
  border: 1px solid #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

</style>

<script>
export default {
data() {
  return {
    title: '',
    description: '',
    file: '',
    message: ''
  }
},
methods: {
  handleFileUpload() {
    this.file = this.$refs.file.files[0];
  },
  submitPost() {
    let formData = new FormData();
    formData.append('title', this.title);
    formData.append('description', this.description);
    formData.append('file', this.file);

    fetch('http://127.0.0.1:5000/post', {
      method: 'POST',
      headers: {  // Add this headers option
        'Authorization': 'Bearer ' + this.$store.state.token  // Replace this with your method of accessing the token
      },
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      this.message = data.message;
    })
  }
}
}
</script>
