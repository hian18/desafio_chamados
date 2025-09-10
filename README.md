# OpenTicket

Sistema de gestão de tickets com interface web responsiva, API REST e notificações em tempo real.

## 🚀 Tecnologias

### Backend
- **Django 5.2** - Framework web Python
- **Django REST Framework** - API REST
- **Django Channels** - WebSockets para notificações
- **SQLite** - Banco de dados
- **JWT** - Autenticação
- **drf-spectacular** - Documentação da API

### Frontend
- **Vue.js 3** - Framework JavaScript
- **Vite** - Build tool
- **Bootstrap 5** - UI framework
- **Bootstrap Icons** - Ícones

## 📋 Pré-requisitos

- Python 3.10+
- Node.js 16+
- npm ou yarn

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd openticket
```

### 2. Backend (Django)

```bash
cd backend

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Criar usuários e tickets de teste
python manage.py shell < create_test_tickets.py 

# Executar servidor
python manage.py runserver
```

### 3. Frontend (Vue.js)

```bash
cd frontend

# Instalar dependências
npm install

# Executar servidor de desenvolvimento
npm run dev
```

## 🔑 Credenciais de Teste

- **Agent:** `agent@cloudpark.com` / `123`
- **Technician:** `technician@cloudpark.com` / `123`

## 📱 Acesso

- **Frontend Vue:** http://localhost:5173
- **Backend Django:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs/

### 🎨 Interface
- Design responsivo (mobile, tablet, desktop)
- Tema moderno com gradientes
- Ícones Bootstrap
- Notificações toast
- Modais interativos

## 📊 Estrutura do Projeto

```
openticket/
├── backend/                 # Django API
│   ├── api/                # API REST
│   ├── core/               # Modelos principais
│   ├── front/              # Templates Django
│   ├── services/           # Serviços (WebSocket, permissões)
│   └── config/             # Configurações Django
├── frontend/               # Vue.js SPA
│   ├── src/
│   │   ├── components/     # Componentes Vue
│   │   ├── views/          # Páginas
│   │   ├── stores/         # Pinia stores
│   │   └── services/       # Serviços API
└── README.md
```

## 🌐 API Endpoints

### Autenticação
- `POST /api/token/` - Login
- `POST /api/token/refresh/` - Refresh token

### Tickets
- `GET /api/v1/tickets/` - Listar tickets
- `GET /api/v1/tickets/{id}/` - Detalhes do ticket
- `PATCH /api/v1/tickets/{id}/` - Atualizar ticket
- `POST /api/v1/tickets/{id}/resolve/` - Resolver ticket
- `GET /api/v1/tickets/stats/` - Estatísticas

## 🎨 Customização

### Cores e Tema
- Edite os gradientes em `frontend/src/views/Login.vue` e `Dashboard.vue`
- Modifique as cores dos badges de status/prioridade

### Traduções
- Arquivo: `backend/locale/pt_BR/LC_MESSAGES/django.po`
- Compile com: `python manage.py compilemessages`
