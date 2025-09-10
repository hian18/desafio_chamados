<template>
  <div class="login-container">
    <div class="login-wrapper">
      <!-- Left side - Branding -->
      <div class="login-branding">
        <div class="branding-content">
          <div class="brand-logo">
            <img :src="logoUrl" alt="OpenTicket" />
          </div>
          <p class="brand-subtitle">Sistema de Gestão de Tickets</p>
          <div class="brand-features">
            <div class="feature-item">
              <i class="bi bi-check-circle"></i>
              <span>Gestão completa de tickets</span>
            </div>
            <div class="feature-item">
              <i class="bi bi-check-circle"></i>
              <span>Interface intuitiva</span>
            </div>
            <div class="feature-item">
              <i class="bi bi-check-circle"></i>
              <span>Notifiações em tempo real</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right side - Login Form -->
      <div class="login-form-section">
        <div class="login-form-container">
          <div class="form-header">
            <h2 class="form-title">Bem-vindo de volta</h2>
            <p class="form-subtitle">Faça login para acessar o sistema</p>
          </div>

          <form @submit.prevent="handleLogin" class="login-form">
            <div class="form-group">
              <label for="email" class="form-label">Email</label>
              <div class="input-group">
                <span class="input-group-text">
                  <i class="bi bi-envelope"></i>
                </span>
                <input
                  type="email"
                  id="email"
                  v-model="form.email"
                  class="form-control"
                  :class="{ 'is-invalid': errors.email }"
                  placeholder="Digite seu email"
                  required
                />
              </div>
              <div v-if="errors.email" class="invalid-feedback">
                {{ errors.email }}
              </div>
            </div>

            <div class="form-group">
              <label for="password" class="form-label">Senha</label>
              <div class="input-group">
                <span class="input-group-text">
                  <i class="bi bi-lock"></i>
                </span>
                <input
                  type="password"
                  id="password"
                  v-model="form.password"
                  class="form-control"
                  :class="{ 'is-invalid': errors.password }"
                  placeholder="Digite sua senha"
                  required
                />
              </div>
              <div v-if="errors.password" class="invalid-feedback">
                {{ errors.password }}
              </div>
            </div>

            <div v-if="error" class="alert alert-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              {{ error }}
            </div>

            <button
              type="submit"
              class="btn btn-primary btn-login"
              :disabled="loading"
            >
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-box-arrow-in-right me-2"></i>
              {{ loading ? 'Entrando...' : 'Entrar' }}
            </button>
          </form>

          <div class="login-footer">
            <div class="demo-credentials">
              <h6>Credenciais de teste:</h6>
              <div class="credential-item">
                <strong>Email:</strong> technician@cloudpark.com
              </div>
              <div class="credential-item">
                <strong>Senha:</strong> 123
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import logoAsset from '@/assets/Logo-Padrao.png'

export default {
  name: 'Login',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    return {
      authStore,
      router
    }
  },
  data() {
    return {
      logoUrl: logoAsset,
      form: {
        email: '',
        password: ''
      },
      errors: {},
      error: '',
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''
      this.errors = {}

      // Basic validation
      if (!this.form.email) {
        this.errors.email = 'Email é obrigatório'
      }
      if (!this.form.password) {
        this.errors.password = 'Senha é obrigatória'
      }

      if (Object.keys(this.errors).length > 0) {
        this.loading = false
        return
      }

      const result = await this.authStore.login(this.form)
      
      if (result.success) {
        this.router.push('/dashboard')
      } else {
        this.error = result.error
      }
      
      this.loading = false
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-wrapper {
  display: flex;
  width: 100%;
  max-width: 1000px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  min-height: 600px;
}

/* Left side - Branding */
.login-branding {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 40px;
  position: relative;
}

.login-branding::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="10" cy="60" r="0.5" fill="white" opacity="0.1"/><circle cx="90" cy="40" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.3;
}

.branding-content {
  text-align: center;
  color: white;
  position: relative;
  z-index: 1;
}

.brand-logo {
  margin-bottom: 20px;
}

.brand-logo img {
  height: 96px;
  width: auto;
  filter: drop-shadow(0 2px 6px rgba(0,0,0,0.2));
}

.brand-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 15px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.brand-subtitle {
  font-size: 1.2rem;
  margin-bottom: 40px;
  opacity: 0.9;
  font-weight: 300;
}

.brand-features {
  text-align: left;
  max-width: 300px;
  margin: 0 auto;
}

.feature-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  font-size: 1rem;
}

.feature-item i {
  margin-right: 12px;
  font-size: 1.1rem;
  color: #4ade80;
}

/* Right side - Login Form */
.login-form-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 40px;
  background: white;
}

.login-form-container {
  width: 100%;
  max-width: 400px;
}

.form-header {
  text-align: center;
  margin-bottom: 40px;
}

.form-title {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 10px;
}

.form-subtitle {
  color: #666;
  font-size: 1rem;
  margin: 0;
}

.login-form {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 25px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
}

.input-group {
  position: relative;
}

.input-group-text {
  background: #f8f9fa;
  border: 1px solid #e1e5e9;
  border-right: none;
  color: #667eea;
  padding: 0 15px;
  border-radius: 8px 0 0 8px;
}

.form-control {
  border: 1px solid #e1e5e9;
  border-left: none;
  border-radius: 0 8px 8px 0;
  padding: 15px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.form-control:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-control.is-invalid {
  border-color: #dc3545;
}

.invalid-feedback {
  display: block;
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 5px;
}

.btn-login {
  width: 100%;
  padding: 15px;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.login-footer {
  text-align: center;
  padding-top: 30px;
  border-top: 1px solid #e1e5e9;
}

.demo-credentials {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e1e5e9;
}

.demo-credentials h6 {
  color: #333;
  margin-bottom: 15px;
  font-weight: 600;
}

.credential-item {
  margin-bottom: 8px;
  font-size: 0.9rem;
  color: #666;
}

.credential-item strong {
  color: #333;
}

.alert {
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  border: none;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

/* Desktop-only layout - no responsive adjustments */
.login-wrapper {
  flex-direction: row !important;
  max-width: 1000px !important;
}

.login-branding {
  padding: 60px 40px !important;
}

.login-form-section {
  padding: 60px 40px !important;
}
</style>
