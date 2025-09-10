import { ref, onMounted, onUnmounted } from 'vue'

export function useWebSocket() {
  const socket = ref(null)
  const isConnected = ref(false)
  const notifications = ref([])

  const connect = () => {
    // Força o WebSocket a conectar no backend Django (porta 8000)
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${wsProtocol}//localhost:8000/ws/tickets/`
    
    socket.value = new WebSocket(wsUrl)

    socket.value.onopen = () => {
      console.log('WebSocket connection established')
      isConnected.value = true
    }

    socket.value.onmessage = (event) => {
      const data = JSON.parse(event.data)
      handleMessage(data)
    }

    socket.value.onclose = () => {
      console.log('WebSocket connection closed')
      isConnected.value = false
      // Try to reconnect after 5 seconds
      setTimeout(() => {
        if (socket.value?.readyState === WebSocket.CLOSED) {
          connect()
        }
      }, 5000)
    }

    socket.value.onerror = (error) => {
      console.error('WebSocket error:', error)
      isConnected.value = false
    }
  }

  const handleMessage = (data) => {
    if (data.type === 'ticket_created') {
      addNotification({
        type: 'success',
        title: 'Novo Ticket',
        message: `Ticket #${data.ticket.id} foi criado: ${data.ticket.title}`,
        ticket: data.ticket
      })
    } else if (data.type === 'ticket_updated') {
      addNotification({
        type: 'info',
        title: 'Ticket Atualizado',
        message: `Ticket #${data.ticket.id} foi atualizado`,
        ticket: data.ticket
      })
    } else if (data.type === 'ticket_resolved') {
      addNotification({
        type: 'success',
        title: 'Ticket Resolvido',
        message: `Ticket #${data.ticket.id} foi resolvido`,
        ticket: data.ticket
      })
    } else if (data.type === 'custom_notification') {
      addNotification({
        type: data.notification_type || 'info',
        title: 'Notificação',
        message: data.message
      })
    }
  }

  const addNotification = (notification) => {
    const id = Date.now()
    notifications.value.push({
      id,
      ...notification,
      timestamp: new Date()
    })

    // Auto remove after 5 seconds
    setTimeout(() => {
      removeNotification(id)
    }, 5000)
  }

  const removeNotification = (id) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const disconnect = () => {
    if (socket.value) {
      socket.value.close()
      socket.value = null
      isConnected.value = false
    }
  }

  onMounted(() => {
    connect()
  })

  onUnmounted(() => {
    disconnect()
  })

  return {
    socket,
    isConnected,
    notifications,
    connect,
    disconnect,
    addNotification,
    removeNotification
  }
}
