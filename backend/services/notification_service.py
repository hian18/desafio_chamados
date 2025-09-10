from .websocket_service import WebSocketNotificationService


class NotificationService:
    """Serviço para gerenciar notificações do sistema"""
    
    @classmethod
    def notify_ticket_created(cls, ticket):
        """Notifica criação de ticket"""
        WebSocketNotificationService.send_ticket_created(ticket)
    
    @classmethod
    def notify_ticket_updated(cls, ticket):
        """Notifica atualização de ticket"""
        WebSocketNotificationService.send_ticket_updated(ticket)
    
    @classmethod
    def notify_ticket_resolved(cls, ticket):
        """Notifica resolução de ticket"""
        WebSocketNotificationService.send_ticket_resolved(ticket)
    
    @classmethod
    def notify_system_message(cls, message, message_type='info'):
        """Notifica mensagem do sistema"""
        WebSocketNotificationService.send_custom_notification(message, message_type)
    
    @classmethod
    def notify_user_action(cls, user, action, target=None):
        """
        Notifica ação de usuário
        
        Args:
            user: Usuário que executou a ação
            action (str): Ação executada
            target: Objeto alvo da ação (opcional)
        """
        message = f"Usuário {user.username} executou: {action}"
        if target:
            message += f" em {target}"
        
        cls.notify_system_message(message, 'info')
    
    @classmethod
    def notify_error(cls, error_message):
        """Notifica erro do sistema"""
        cls.notify_system_message(f"Erro: {error_message}", 'error')
    
    @classmethod
    def notify_success(cls, success_message):
        """Notifica sucesso"""
        cls.notify_system_message(success_message, 'success')
    
    @classmethod
    def notify_warning(cls, warning_message):
        """Notifica aviso"""
        cls.notify_system_message(warning_message, 'warning')
