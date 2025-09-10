<template>
  <div class="notification-container">
    <TransitionGroup name="notification" tag="div">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        :class="['alert', `alert-${notification.type}`, 'alert-dismissible', 'fade', 'show', 'notification-toast']"
        role="alert"
      >
        <div class="notification-content">
          <div class="notification-header">
            <strong>{{ notification.title }}</strong>
            <button
              type="button"
              class="btn-close"
              @click="removeNotification(notification.id)"
              aria-label="Close"
            ></button>
          </div>
          <div class="notification-body">
            {{ notification.message }}
          </div>
          <div class="notification-time">
            {{ formatTime(notification.timestamp) }}
          </div>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script>
export default {
  name: 'NotificationToast',
  props: {
    notifications: {
      type: Array,
      default: () => []
    }
  },
  emits: ['remove-notification'],
  methods: {
    removeNotification(id) {
      this.$emit('remove-notification', id)
    },
    formatTime(timestamp) {
      return new Date(timestamp).toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.notification-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  max-width: 400px;
}

.notification-toast {
  margin-bottom: 10px;
  min-width: 300px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border: none;
  border-radius: 8px;
}

.notification-content {
  display: flex;
  flex-direction: column;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.notification-body {
  font-size: 0.9rem;
  margin-bottom: 4px;
}

.notification-time {
  font-size: 0.75rem;
  opacity: 0.7;
  text-align: right;
}

.btn-close {
  padding: 0;
  background: none;
  border: none;
  font-size: 1.2rem;
  line-height: 1;
  opacity: 0.5;
  cursor: pointer;
}

.btn-close:hover {
  opacity: 0.75;
}

/* Transition animations */
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-move {
  transition: transform 0.3s ease;
}
</style>
