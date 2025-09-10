import { defineStore } from 'pinia'
import axios from 'axios'

export const useTicketsStore = defineStore('tickets', {
  state: () => ({
    tickets: [],
    currentTicket: null,
    loading: false,
    error: null,
    stats: {
      total: 0,
      open: 0,
      in_progress: 0,
      pending: 0,
      resolved: 0,
      cancelled: 0
    }
  }),

  getters: {
    getTicketById: (state) => (id) => {
      return state.tickets.find(ticket => ticket.id === id)
    },
    
    getTicketsByStatus: (state) => (status) => {
      return state.tickets.filter(ticket => ticket.status === status)
    }
  },

  actions: {
    async fetchTickets(params = {}) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('http://localhost:8000/api/v1/tickets/', { params })
        this.tickets = response.data.results || response.data
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Fetch tickets error:', error)
        this.error = error.response?.data?.detail || 'Erro ao carregar tickets'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchTicket(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`http://localhost:8000/api/v1/tickets/${id}/`)
        this.currentTicket = response.data
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Fetch ticket error:', error)
        this.error = error.response?.data?.detail || 'Erro ao carregar ticket'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async createTicket(ticketData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('http://localhost:8000/api/v1/tickets/', ticketData)
        this.tickets.unshift(response.data)
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Create ticket error:', error)
        this.error = error.response?.data?.detail || 'Erro ao criar ticket'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async updateTicket(id, ticketData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.patch(`http://localhost:8000/api/v1/tickets/${id}/`, ticketData)
        
        // Update ticket in the list
        const index = this.tickets.findIndex(ticket => ticket.id === id)
        if (index !== -1) {
          this.tickets[index] = response.data
        }
        
        // Update current ticket if it's the same
        if (this.currentTicket && this.currentTicket.id === id) {
          this.currentTicket = response.data
        }
        
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Update ticket error:', error)
        this.error = error.response?.data?.detail || 'Erro ao atualizar ticket'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async resolveTicket(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post(`http://localhost:8000/api/v1/tickets/${id}/resolve/`)
        
        // Update ticket in the list
        const index = this.tickets.findIndex(ticket => ticket.id === id)
        if (index !== -1) {
          this.tickets[index] = response.data
        }
        
        // Update current ticket if it's the same
        if (this.currentTicket && this.currentTicket.id === id) {
          this.currentTicket = response.data
        }
        
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Resolve ticket error:', error)
        this.error = error.response?.data?.detail || 'Erro ao resolver ticket'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchStats() {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/tickets/stats/')
        this.stats = response.data
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Fetch stats error:', error)
        return { success: false, error: error.response?.data?.detail || 'Erro ao carregar estatísticas' }
      }
    },

    clearCurrentTicket() {
      this.currentTicket = null
    },

    clearError() {
      this.error = null
    }
  }
})
