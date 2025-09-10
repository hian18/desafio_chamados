#!/usr/bin/env python
"""
Script para criar tickets de teste
Execute: python manage.py shell < create_test_tickets.py
"""

import random
from datetime import datetime, timedelta
from django.utils import timezone
from core.models import Ticket, CustomUser, TicketStatus

# Dados para gerar tickets aleatórios
TITLES = [
    "Problema com login no sistema",
    "Erro ao carregar relatórios",
    "Solicitação de acesso ao banco de dados",
    "Falha na impressão de documentos",
    "Atualização de software necessária",
    "Problema com conexão de rede",
    "Solicitação de nova conta de usuário",
    "Erro no sistema de backup",
    "Problema com email corporativo",
    "Solicitação de instalação de software",
    "Falha no sistema de monitoramento",
    "Problema com servidor de arquivos",
    "Solicitação de reset de senha",
    "Erro na aplicação web",
    "Problema com impressora",
    "Solicitação de acesso remoto",
    "Falha no sistema de autenticação",
    "Problema com banco de dados",
    "Solicitação de configuração de VPN",
    "Erro no sistema de logs",
]

DESCRIPTIONS = [
    "O usuário está relatando problemas para fazer login no sistema principal. Erro aparece após inserir credenciais.",
    "Relatórios não estão carregando corretamente. Página fica em branco após selecionar período.",
    "Funcionário precisa de acesso ao banco de dados para consultas específicas do departamento.",
    "Impressora não está respondendo. Documentos ficam na fila mas não são impressos.",
    "Sistema operacional precisa ser atualizado para versão mais recente por questões de segurança.",
    "Conexão de rede está instável. Perda de conectividade intermitente durante o dia.",
    "Novo funcionário precisa de conta de usuário criada no sistema corporativo.",
    "Sistema de backup automático falhou durante a noite. Verificação necessária.",
    "Email corporativo não está recebendo mensagens externas. Configuração pode estar incorreta.",
    "Departamento solicita instalação de software específico para análise de dados.",
    "Sistema de monitoramento não está reportando status correto dos servidores.",
    "Usuários não conseguem acessar arquivos compartilhados no servidor principal.",
    "Funcionário esqueceu senha e precisa de reset para acessar sistemas.",
    "Aplicação web está apresentando erro 500 em algumas funcionalidades.",
    "Impressora multifuncional está com problema no scanner. Apenas impressão funciona.",
    "Funcionário precisa de acesso remoto para trabalhar de casa.",
    "Sistema de autenticação está rejeitando usuários válidos ocasionalmente.",
    "Banco de dados está com performance degradada. Consultas estão lentas.",
    "Configuração de VPN necessária para novo escritório remoto.",
    "Sistema de logs não está registrando eventos corretamente.",
]

DEPARTMENTS = ["TI", "RH", "Financeiro", "Vendas", "Marketing", "Operações", "Jurídico", "Comercial", "Suporte"]

PRIORITIES = ['low', 'medium', 'high', 'urgent']
STATUSES = [TicketStatus.OPEN.value, TicketStatus.IN_PROGRESS.value, TicketStatus.RESOLVED.value]


def create_test_users():
    """Cria usuários de teste se não existirem"""
    from django.contrib.auth.hashers import make_password

    # Usuários de teste
    test_users = [
        {
            'username': 'agent@cloudpark.com',
            'email': 'agent@cloudpark.com',
            'first_name': 'Joao',
            'last_name': '',
            'role': 'agent',
            'password': '123',
        },
        {
            'username': 'technician@cloudpark.com',
            'email': 'technician@cloudpark.com',
            'first_name': 'Maria',
            'last_name': '',
            'role': 'technician',
            'password': '123',
        },
    ]

    created_users = []
    for user_data in test_users:
        user, created = CustomUser.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'username': user_data['username'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'role': user_data['role'],
                'password': make_password(user_data['password']),
                'is_active': True,
            },
        )
        if created:
            print(f"✅ Usuário criado: {user_data['email']}")
        else:
            print(f"👤 Usuário já existe: {user_data['email']}")
        created_users.append(user)

    return created_users


def create_test_tickets():
    """Cria 20 tickets de teste"""

    # Cria usuários de teste primeiro
    print("👥 Verificando/criando usuários de teste...")
    test_users = create_test_users()

    # Busca todos os usuários existentes
    users = list(CustomUser.objects.filter(role='agent'))
    if not users:
        print("❌ Nenhum usuário encontrado.")
        return

    print(f"📝 Criando 20 tickets de teste...")
    print(f"👥 Usando {len(users)} usuários disponíveis")

    created_count = 0

    for i in range(20):
        # Seleciona dados aleatórios
        title = random.choice(TITLES)
        description = random.choice(DESCRIPTIONS)
        department = random.choice(DEPARTMENTS)
        priority = random.choice(PRIORITIES)
        status = random.choice(STATUSES)

        # Usuário criador aleatório
        created_by = random.choice(users)

        # Usuário atribuído (pode ser None ou um usuário aleatório)
        assigned_to = random.choice(users) if random.choice([True, False]) else None

        # Data de criação aleatória (últimos 30 dias)
        days_ago = random.randint(0, 30)
        created_at = timezone.now() - timedelta(days=days_ago)

        # Cria o ticket
        ticket = Ticket.objects.create(
            title=title,
            description=description,
            department=department,
            priority=priority,
            status=status,
            created_by=created_by,
            assigned_to=assigned_to,
            created_at=created_at,
        )

        created_count += 1
        print(f"✅ Ticket #{ticket.id} criado: {title[:50]}...")

    print(f"\n🎉 {created_count} tickets criados com sucesso!")
    print(f"📊 Estatísticas:")
    print(f"   - Total de tickets: {Ticket.objects.count()}")
    print(f"   - Status Open: {Ticket.objects.filter(status='open').count()}")
    print(f"   - Status In Progress: {Ticket.objects.filter(status='in_progress').count()}")
    print(f"   - Status Resolved: {Ticket.objects.filter(status='resolved').count()}")


create_test_tickets()
