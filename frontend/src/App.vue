<template>
  <div>
    <router-view />
    <NotificationToast 
      :notifications="notifications" 
      @remove-notification="removeNotification"
    />
  </div>
</template>

<script>
import { useWebSocket } from '@/composables/useWebSocket'
import NotificationToast from '@/components/NotificationToast.vue'

export default {
  name: 'App',
  components: {
    NotificationToast
  },
  setup() {
    const { notifications, removeNotification } = useWebSocket()
    
    return {
      notifications,
      removeNotification
    }
  }
}
</script>

<style>
/* Bootstrap Icons - must be first */
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css');

/* Global styles - Responsive */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  width: 100%;
  font-size: 14px;
  line-height: 1.5;
}

* {
  box-sizing: border-box;
}

/* Responsive containers */
.container-fluid {
  width: 100%;
  padding-left: 1rem;
  padding-right: 1rem;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

/* Mobile first approach */
@media (max-width: 768px) {
  .container-fluid {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
  
  .container {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
  
  body {
    font-size: 13px;
  }
}

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) {
  .container-fluid {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}

/* Desktop */
@media (min-width: 1025px) {
  .container-fluid {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
}
</style>