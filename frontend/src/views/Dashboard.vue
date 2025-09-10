<template>
  <div class="dashboard">
    <!-- Header -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="dashboard-title">
            <i class="bi bi-house"></i>
            Dashboard
          </h1>
        </div>
        <div class="header-right">
          <button @click="testNotification" class="btn btn-outline-info me-2">
            <i class="bi bi-bell"></i>
            Testar Notificação
          </button>
          <button @click="logout" class="btn btn-outline-danger">
            <i class="bi bi-box-arrow-right"></i>
            Sair
          </button>
        </div>
      </div>
    </header>

    <!-- Stats Cards -->
    <div class="stats-section">
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-card">
            <div class="stat-icon bg-primary">
              <i class="bi bi-ticket-perforated"></i>
            </div>
            <div class="stat-content">
              <h3>{{ stats.total }}</h3>
              <p>Total</p>
            </div>
          </div>
        </div>
        <div class="stat-item">
          <div class="stat-card">
            <div class="stat-icon bg-success">
              <i class="bi bi-circle"></i>
            </div>
            <div class="stat-content">
              <h3>{{ stats.open }}</h3>
              <p>Abertos</p>
            </div>
          </div>
        </div>
        <div class="stat-item">
          <div class="stat-card">
            <div class="stat-icon bg-info">
              <i class="bi bi-arrow-clockwise"></i>
            </div>
            <div class="stat-content">
              <h3>{{ stats.in_progress }}</h3>
              <p>Em Progresso</p>
            </div>
          </div>
        </div>
        
        <div class="stat-item">
          <div class="stat-card">
            <div class="stat-icon bg-success">
              <i class="bi bi-check-circle"></i>
            </div>
            <div class="stat-content">
              <h3>{{ stats.resolved }}</h3>
              <p>Resolvidos</p>
            </div>
          </div>
        </div>
        <div class="stat-item">
          <div class="stat-card">
            <div class="stat-icon bg-danger">
              <i class="bi bi-x-circle"></i>
            </div>
            <div class="stat-content">
              <h3>{{ stats.cancelled }}</h3>
              <p>Cancelados</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-section">
      <div class="filters-card">
        <div class="filters-grid">
          <div class="filter-item">
            <label class="form-label">Status</label>
            <select v-model="filters.status" @change="applyFilters" class="form-select">
              <option value="">Todos</option>
              <option value="open">Aberto</option>
              <option value="in_progress">Em Progresso</option>
              <option value="resolved">Resolvido</option>
              <option value="cancelled">Cancelado</option>
            </select>
          </div>
          <div class="filter-item">
            <label class="form-label">Prioridade</label>
            <select v-model="filters.priority" @change="applyFilters" class="form-select">
              <option value="">Todas</option>
              <option value="low">Baixa</option>
              <option value="medium">Média</option>
              <option value="high">Alta</option>
              <option value="urgent">Urgente</option>
            </select>
          </div>
          <div class="filter-item filter-search">
            <label class="form-label">Buscar</label>
            <input
              v-model="filters.search"
              @input="debounceSearch"
              type="text"
              class="form-control"
              placeholder="Buscar por título, descrição ou ID..."
            />
          </div>
          <div class="filter-item">
            <label class="form-label">&nbsp;</label>
            <button @click="clearFilters" class="btn btn-outline-secondary w-100">
              <i class="bi bi-x-circle"></i>
              Limpar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Tickets Table -->
    <div class="table-section">
      <div class="table-card">
        <div class="card-header">
          <h5 class="mb-0">Tickets</h5>
        </div>
        <div class="card-body p-0">
          <div v-if="loading" class="text-center p-4">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Carregando...</span>
            </div>
          </div>
          
          <div v-else-if="tickets.length === 0" class="text-center p-4">
            <i class="bi bi-inbox display-1 text-muted"></i>
            <p class="text-muted mt-3">Nenhum ticket encontrado</p>
          </div>
          
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>ID</th>
                  <th>Título</th>
                  <th>Status</th>
                  <th>Prioridade</th>
                  <th>Departamento</th>
                  <th>Criado em</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="ticket in tickets" :key="ticket.id" class="ticket-row">
                  <td>#{{ ticket.id }}</td>
                  <td>
                    <div class="ticket-title" @click="viewTicket(ticket.id)">
                      {{ ticket.title }}
                    </div>
                  </td>
                  <td>
                    <span class="badge" :class="getStatusBadgeClass(ticket.status)">
                      {{ getStatusDisplay(ticket.status) }}
                    </span>
                  </td>
                  <td>
                    <span class="badge" :class="getPriorityBadgeClass(ticket.priority)">
                      {{ getPriorityDisplay(ticket.priority) }}
                    </span>
                  </td>
                  <td>{{ ticket.department || '-' }}</td>
                  <td>{{ formatDate(ticket.created_at) }}</td>
                  <td>
                    <button
                      @click="viewTicket(ticket.id)"
                      class="btn btn-sm btn-outline-primary me-1"
                      title="Ver detalhes"
                    >
                      <i class="bi bi-eye"></i>
                    </button>
                    <button
                      v-if="canResolve(ticket)"
                      @click="showResolveModal(ticket)"
                      class="btn btn-sm btn-success"
                      title="Marcar como resolvido"
                    >
                      <i class="bi bi-check-circle"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Resolve Modal -->
    <div v-if="showModal" class="modal show d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirmar Resolução</h5>
            <button @click="closeModal" type="button" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <p>Tem certeza de que deseja marcar o ticket <strong>#{{ selectedTicket?.id }}</strong> como resolvido?</p>
            <p class="text-muted">{{ selectedTicket?.title }}</p>
          </div>
          <div class="modal-footer">
            <button @click="closeModal" type="button" class="btn btn-secondary">Cancelar</button>
            <button @click="resolveTicket" type="button" class="btn btn-success" :disabled="resolving">
              <span v-if="resolving" class="spinner-border spinner-border-sm me-2"></span>
              {{ resolving ? 'Resolvendo...' : 'Confirmar' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showModal" class="modal-backdrop show"></div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { useTicketsStore } from '@/stores/tickets'
import { useRouter } from 'vue-router'
import { useWebSocket } from '@/composables/useWebSocket'
import notificationService from '@/services/notificationService'

export default {
  name: 'Dashboard',
  setup() {
    const authStore = useAuthStore()
    const ticketsStore = useTicketsStore()
    const router = useRouter()
    const { notifications } = useWebSocket()

    return {
      authStore,
      ticketsStore,
      router,
      notifications
    }
  },
  watch: {
    notifications: {
      handler(newNotifications) {
        if (newNotifications.length > 0) {
          // Reload data when we receive notifications
          this.loadData()
        }
      },
      deep: true
    }
  },
  data() {
    return {
      filters: {
        status: '',
        priority: '',
        search: ''
      },
      showModal: false,
      selectedTicket: null,
      resolving: false,
      searchTimeout: null
    }
  },
  computed: {
    tickets() {
      return this.ticketsStore.tickets
    },
    stats() {
      return this.ticketsStore.stats
    },
    loading() {
      return this.ticketsStore.loading
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      await Promise.all([
        this.ticketsStore.fetchTickets(),
        this.ticketsStore.fetchStats()
      ])
    },
    
    async applyFilters() {
      const params = {}
      if (this.filters.status) params.status = this.filters.status
      if (this.filters.priority) params.priority = this.filters.priority
      if (this.filters.search) params.search = this.filters.search
      
      await this.ticketsStore.fetchTickets(params)
    },
    
    debounceSearch() {
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => {
        this.applyFilters()
      }, 500)
    },
    
    clearFilters() {
      this.filters = {
        status: '',
        priority: '',
        search: ''
      }
      this.applyFilters()
    },
    
    viewTicket(id) {
      this.router.push(`/ticket/${id}`)
    },
    
    canResolve(ticket) {
      return ticket.status === 'open' || ticket.status === 'in_progress' || ticket.status === 'pending'
    },
    
    showResolveModal(ticket) {
      this.selectedTicket = ticket
      this.showModal = true
    },
    
    closeModal() {
      this.showModal = false
      this.selectedTicket = null
    },
    
    async resolveTicket() {
      if (!this.selectedTicket) return
      
      this.resolving = true
      const result = await this.ticketsStore.resolveTicket(this.selectedTicket.id)
      
      if (result.success) {
        this.closeModal()
        await this.loadData() // Reload data to update stats
      } else {
        alert('Erro ao resolver ticket: ' + result.error)
      }
      
      this.resolving = false
    },
    
    logout() {
      this.authStore.logout()
      this.router.push('/login')
    },
    
    async testNotification() {
      try {
        await notificationService.sendSuccessNotification('Esta é uma notificação de teste!')
      } catch (error) {
        console.error('Erro ao enviar notificação:', error)
      }
    },
    
    getStatusBadgeClass(status) {
      const classes = {
        'open': 'bg-success',
        'in_progress': 'bg-primary',
        'pending': 'bg-warning',
        'resolved': 'bg-info',
        'cancelled': 'bg-danger'
      }
      return classes[status] || 'bg-secondary'
    },
    
    getPriorityBadgeClass(priority) {
      const classes = {
        'low': 'bg-success',
        'medium': 'bg-primary',
        'high': 'bg-warning',
        'urgent': 'bg-danger'
      }
      return classes[priority] || 'bg-secondary'
    },
    
    getStatusDisplay(status) {
      const displays = {
        'open': 'Aberto',
        'in_progress': 'Em Progresso',
        'pending': 'Pendente',
        'resolved': 'Resolvido',
        'cancelled': 'Cancelado'
      }
      return displays[status] || status
    },
    
    getPriorityDisplay(priority) {
      const displays = {
        'low': 'Baixa',
        'medium': 'Média',
        'high': 'Alta',
        'urgent': 'Urgente'
      }
      return displays[priority] || priority
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: #f8f9fa;
  width: 100%;
  max-width: none;
  margin: 0;
  padding: 0;
}

.dashboard-header {
  background: white;
  border-bottom: 1px solid #dee2e6;
  padding: 1.5rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;
  max-width: 100%;
}

.header-left {
  flex: 1;
}

.header-right {
  flex-shrink: 0;
}

.dashboard-title {
  margin: 0;
  color: #333;
  font-size: 1.8rem;
  font-weight: 600;
}

.dashboard-title i {
  color: #667eea;
  margin-right: 12px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid #e9ecef;
  min-height: 100px;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 18px;
  color: white;
  font-size: 1.75rem;
}

.stat-content h3 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
  line-height: 1;
}

.stat-content p {
  margin: 4px 0 0 0;
  color: #666;
  font-size: 0.85rem;
  font-weight: 500;
}

.ticket-row {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.ticket-row:hover {
  background-color: #f8f9fa;
}

.ticket-title {
  cursor: pointer;
  color: #667eea;
  font-weight: 500;
  transition: color 0.2s ease;
}

.ticket-title:hover {
  color: #5a6fd8;
  text-decoration: underline;
}

.badge {
  font-size: 0.8rem;
  padding: 0.4rem 0.8rem;
  font-weight: 500;
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
  background-color: #f8f9fa;
  padding: 0.75rem 0.5rem;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.table td {
  padding: 0.75rem 0.5rem;
  vertical-align: middle;
  border-top: 1px solid #e9ecef;
  font-size: 0.9rem;
}

.modal-backdrop {
  opacity: 0.5;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
  border-radius: 6px;
}

.card {
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-radius: 12px;
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  font-weight: 600;
  padding: 1rem 1.25rem;
  border-radius: 12px 12px 0 0 !important;
  font-size: 0.95rem;
}

.card-body {
  padding: 1.25rem;
}

.form-control, .form-select {
  border-radius: 8px;
  border: 1px solid #ced4da;
  padding: 0.6rem 0.8rem;
  font-size: 0.9rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-control:focus, .form-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.btn {
  border-radius: 8px;
  font-weight: 500;
  padding: 0.6rem 1.25rem;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.btn:hover {
  transform: translateY(-1px);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}

.btn-success {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  border: none;
}

.btn-success:hover {
  background: linear-gradient(135deg, #218838 0%, #1ea085 100%);
}

.btn-outline-danger {
  border-color: #dc3545;
  color: #dc3545;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  border-color: #dc3545;
}

.btn-outline-secondary {
  border-color: #6c757d;
  color: #6c757d;
}

.btn-outline-secondary:hover {
  background-color: #6c757d;
  border-color: #6c757d;
}

/* Global container overrides */
.container-fluid {
  max-width: 100% !important;
  width: 100% !important;
  padding-left: 1rem;
  padding-right: 1rem;
}

/* Stats Section */
.stats-section {
  padding: 1rem;
  width: 100%;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
  width: 100%;
}

.stat-item {
  width: 100%;
}

/* Filters Section */
.filters-section {
  padding: 0 1rem 1rem 1rem;
  width: 100%;
}

.filters-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  width: 100%;
}

.filters-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 2fr 1fr;
  gap: 1rem;
  width: 100%;
}

.filter-item {
  width: 100%;
}

.filter-search {
  grid-column: span 2;
}

/* Table Section */
.table-section {
  padding: 0 1rem 1rem 1rem;
  width: 100%;
}

.table-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  width: 100%;
  overflow: hidden;
}

/* Mobile responsive layout */
@media (max-width: 768px) {
  .dashboard {
    padding: 0;
  }
  
  .dashboard-header {
    padding: 1rem 0;
  }
  
  .header-content {
    flex-direction: column !important;
    gap: 1rem;
    align-items: stretch !important;
  }
  
  .header-right {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
  }
  
  .dashboard-title {
    font-size: 1.5rem;
    text-align: center;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 0.75rem !important;
  }
  
  .stat-card {
    padding: 1rem;
    min-height: 80px;
  }
  
  .stat-icon {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
    margin-right: 12px;
  }
  
  .stat-content h3 {
    font-size: 1.3rem;
  }
  
  .stat-content p {
    font-size: 0.75rem;
  }
  
  .filters-grid {
    grid-template-columns: 1fr !important;
    gap: 0.75rem !important;
  }
  
  .filter-search {
    grid-column: span 1 !important;
  }
  
  .table-responsive {
    font-size: 0.8rem;
  }
  
  .table th, .table td {
    padding: 0.5rem 0.25rem;
  }
  
  .btn-sm {
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
  }
  
  .modal-dialog {
    margin: 1rem;
  }
}

/* Tablet responsive layout */
@media (min-width: 769px) and (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr) !important;
    gap: 1rem !important;
  }
  
  .filters-grid {
    grid-template-columns: 1fr 1fr !important;
    gap: 1rem !important;
  }
  
  .filter-search {
    grid-column: span 2 !important;
  }
  
  .header-content {
    flex-direction: row !important;
    justify-content: space-between !important;
    align-items: center !important;
  }
}

/* Desktop layout */
@media (min-width: 1025px) {
  .stats-grid {
    grid-template-columns: repeat(5, 1fr) !important;
    gap: 1rem !important;
  }
  
  .filters-grid {
    grid-template-columns: 1fr 1fr 2fr 1fr !important;
    gap: 1rem !important;
  }
  
  .filter-search {
    grid-column: span 1 !important;
  }
  
  .header-content {
    flex-direction: row !important;
    justify-content: space-between !important;
    align-items: center !important;
  }
}

/* Large desktop optimizations */
@media (min-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(5, 1fr) !important;
  }
  
  .stat-card {
    padding: 20px;
  }
  
  .stat-icon {
    width: 60px;
    height: 60px;
    font-size: 1.75rem;
  }
  
  .stat-content h3 {
    font-size: 1.8rem;
  }
}
</style>
