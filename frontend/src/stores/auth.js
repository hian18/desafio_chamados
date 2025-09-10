import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false
  }),

  getters: {
    isLoggedIn: (state) => state.isAuthenticated && state.token
  },

  actions: {
    async login(credentials) {
      try {
        const response = await axios.post('http://localhost:8000/api/token/', credentials)
        const { access, refresh } = response.data
        
        this.token = access
        this.isAuthenticated = true
        localStorage.setItem('token', access)
        localStorage.setItem('refresh', refresh)
        
        // Set default authorization header
        axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
        
        // Get user info
        await this.getUserInfo()
        
        return { success: true }
      } catch (error) {
        console.error('Login error:', error)
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Erro ao fazer login' 
        }
      }
    },

    async getUserInfo() {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/tickets/')
        // Since we don't have a user endpoint, we'll use the tickets endpoint to verify auth
        this.user = { username: 'User' } // Placeholder
        return true
      } catch (error) {
        console.error('Get user info error:', error)
        this.logout()
        return false
      }
    },

    async refreshToken() {
      try {
        const refresh = localStorage.getItem('refresh')
        if (!refresh) {
          this.logout()
          return false
        }

        const response = await axios.post('http://localhost:8000/api/token/refresh/', {
          refresh: refresh
        })
        
        const { access } = response.data
        this.token = access
        localStorage.setItem('token', access)
        axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
        
        return true
      } catch (error) {
        console.error('Refresh token error:', error)
        this.logout()
        return false
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
      localStorage.removeItem('refresh')
      delete axios.defaults.headers.common['Authorization']
    },

    initializeAuth() {
      if (this.token) {
        this.isAuthenticated = true
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        this.getUserInfo()
      }
    }
  }
})
