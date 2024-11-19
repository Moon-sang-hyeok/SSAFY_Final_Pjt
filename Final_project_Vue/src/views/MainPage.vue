<template>
    <div class="main-page">
      <h1>Welcome to the Main Page!</h1>
      <p>This is the main page of your application.</p>
      <router-link to="/exchange">Go to Exchange Page</router-link>
    </div>
  </template>
  
  <script>
  export default {
    name: 'MainPage',
  }
  </script>
  
  <style scoped>
  .main-page {
    text-align: center;
    margin-top: 50px;
  }
  </style>
  