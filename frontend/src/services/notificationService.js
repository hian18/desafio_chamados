import axios from 'axios'

const API_URL = 'http://localhost:8000/api/v1'

class NotificationService {
  constructor() {
    this.api = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      }
    })
  }

  setAuthToken(token) {
    this.api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }

  removeAuthToken() {
    delete this.api.defaults.headers.common['Authorization']
  }

  async sendCustomNotification(message, type = 'info') {
    try {
      const response = await this.api.post('/tickets/send_notification/', {
        message,
        type
      })
      return response.data
    } catch (error) {
      console.error('Error sending notification:', error)
      throw error
    }
  }

  async sendSuccessNotification(message) {
    return this.sendCustomNotification(message, 'success')
  }

  async sendErrorNotification(message) {
    return this.sendCustomNotification(message, 'error')
  }

  async sendWarningNotification(message) {
    return this.sendCustomNotification(message, 'warning')
  }

  async sendInfoNotification(message) {
    return this.sendCustomNotification(message, 'info')
  }
}

// Instância global do serviço
const notificationService = new NotificationService()

export default notificationService
