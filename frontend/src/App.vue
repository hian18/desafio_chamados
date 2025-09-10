<template>
  <router-view />
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* Bootstrap Icons - must be first */
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css');

/* Global styles - Desktop optimized */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  width: 100%;
  min-width: 1200px;
  overflow-x: auto;
  font-size: 14px;
}

* {
  box-sizing: border-box;
}

/* Force full width for all containers */
.container-fluid {
  max-width: 100% !important;
  width: 100% !important;
  padding-left: 0.5rem !important;
  padding-right: 0.5rem !important;
}

/* Remove any Bootstrap container limitations */
.container {
  max-width: 100% !important;
  width: 100% !important;
}

/* Override Bootstrap row margins */
.row {
  margin-left: 0 !important;
  margin-right: 0 !important;
}

/* Force all columns to use available space */
.col, .col-1, .col-2, .col-3, .col-4, .col-5, .col-6, 
.col-7, .col-8, .col-9, .col-10, .col-11, .col-12,
.col-auto, .col-sm, .col-md, .col-lg, .col-xl, .col-xxl {
  padding-left: 0.25rem !important;
  padding-right: 0.25rem !important;
}
</style>