<template>
  <div class="ticket-detail">
    <!-- Header -->
    <header class="ticket-header">
      <div class="container-fluid px-4">
        <div class="row align-items-center">
          <div class="col">
            <button @click="goBack" class="btn btn-outline-secondary me-3">
              <i class="bi bi-arrow-left"></i>
              Voltar
            </button>
            <h1 class="ticket-title">
              <i class="bi bi-ticket-perforated"></i>
              Ticket #{{ ticket?.id }}
            </h1>
          </div>
          <div class="col-auto">
            <button @click="logout" class="btn btn-outline-danger">
              <i class="bi bi-box-arrow-right"></i>
              Sair
            </button>
          </div>
        </div>
      </div>
    </header>

    <div class="container-fluid mt-4 px-4">
      <div v-if="loading" class="text-center p-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Carregando...</span>
        </div>
      </div>

      <div v-else-if="error" class="alert alert-danger">
        {{ error }}
      </div>

      <div v-else-if="ticket" class="row">
        <!-- Main Content -->
        <div class="col-lg-8">
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">{{ ticket.title }}</h5>
            </div>
            <div class="card-body">
              <h6>Descrição</h6>
              <p class="text-muted">{{ ticket.description }}</p>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="col-lg-4">
          <div class="card">
            <div class="card-header">
              <h6 class="mb-0">Detalhes do Ticket</h6>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <strong>Status:</strong>
                <span class="badge ms-2" :class="getStatusBadgeClass(ticket.status)">
                  {{ getStatusDisplay(ticket.status) }}
                </span>
              </div>

              <div class="mb-3">
                <strong>Prioridade:</strong>
                <span class="badge ms-2" :class="getPriorityBadgeClass(ticket.priority)">
                  {{ getPriorityDisplay(ticket.priority) }}
                </span>
              </div>

              <div class="mb-3">
                <strong>Departamento:</strong>
                <span class="ms-2">{{ ticket.department || 'Não especificado' }}</span>
              </div>

              <div class="mb-3">
                <strong>Criado por:</strong>
                <span class="ms-2">{{ ticket.created_by?.full_name || ticket.created_by?.username || 'N/A' }}</span>
              </div>

              <div v-if="ticket.assigned_to" class="mb-3">
                <strong>Atribuído para:</strong>
                <span class="ms-2">{{ ticket.assigned_to.full_name || ticket.assigned_to.username }}</span>
              </div>

              <div class="mb-3">
                <strong>Criado em:</strong>
                <span class="ms-2">{{ formatDate(ticket.created_at) }}</span>
              </div>

              <div class="mb-3">
                <strong>Última atualização:</strong>
                <span class="ms-2">{{ formatDate(ticket.updated_at) }}</span>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div v-if="canResolve" class="card mt-3">
            <div class="card-header">
              <h6 class="mb-0">Ações</h6>
            </div>
            <div class="card-body">
              <button
                @click="showResolveModal"
                class="btn btn-success w-100"
                :disabled="resolving"
              >
                <span v-if="resolving" class="spinner-border spinner-border-sm me-2"></span>
                <i class="bi bi-check-circle"></i>
                Marcar como Resolvido
              </button>
            </div>
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
            <p>Tem certeza de que deseja marcar o ticket <strong>#{{ ticket?.id }}</strong> como resolvido?</p>
            <p class="text-muted">{{ ticket?.title }}</p>
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

export default {
  name: 'TicketDetail',
  setup() {
    const authStore = useAuthStore()
    const ticketsStore = useTicketsStore()
    const router = useRouter()

    return {
      authStore,
      ticketsStore,
      router
    }
  },
  data() {
    return {
      showModal: false,
      resolving: false
    }
  },
  computed: {
    ticket() {
      return this.ticketsStore.currentTicket
    },
    loading() {
      return this.ticketsStore.loading
    },
    error() {
      return this.ticketsStore.error
    },
    canResolve() {
      if (!this.ticket) return false
      return this.ticket.status === 'open' || 
             this.ticket.status === 'in_progress' || 
             this.ticket.status === 'pending'
    }
  },
  async mounted() {
    const ticketId = this.$route.params.id
    if (ticketId) {
      await this.ticketsStore.fetchTicket(ticketId)
    }
  },
  methods: {
    goBack() {
      this.router.push('/dashboard')
    },
    
    logout() {
      this.authStore.logout()
      this.router.push('/login')
    },
    
    showResolveModal() {
      this.showModal = true
    },
    
    closeModal() {
      this.showModal = false
    },
    
    async resolveTicket() {
      if (!this.ticket) return
      
      this.resolving = true
      const result = await this.ticketsStore.resolveTicket(this.ticket.id)
      
      if (result.success) {
        this.closeModal()
        // Refresh the ticket data
        await this.ticketsStore.fetchTicket(this.ticket.id)
      } else {
        alert('Erro ao resolver ticket: ' + result.error)
      }
      
      this.resolving = false
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
.ticket-detail {
  min-height: 100vh;
  background-color: #f8f9fa;
  width: 100%;
  max-width: none;
}

.ticket-header {
  background: white;
  border-bottom: 1px solid #dee2e6;
  padding: 1.5rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.ticket-title {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
  font-weight: 600;
  display: inline-block;
}

.ticket-title i {
  color: #667eea;
  margin-right: 12px;
}

.badge {
  font-size: 0.8rem;
  padding: 0.4rem 0.8rem;
  font-weight: 500;
}

.modal-backdrop {
  opacity: 0.5;
}

.card {
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
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

/* Desktop-specific optimizations */
@media (min-width: 1200px) {
  .container-fluid {
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: none;
  }
  
  .card-body {
    padding: 1.25rem;
  }
  
  .card-header {
    padding: 1rem 1.25rem;
  }
}
</style>
