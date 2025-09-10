from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from api.v1.serializers import TicketSerializer


class WebSocketNotificationService:
    """Serviço para enviar notificações via WebSocket"""

    @classmethod
    def send_ticket_notification(cls, notification_type, ticket):
        """
        Envia notificação de ticket via WebSocket

        Args:
            notification_type (str): Tipo da notificação ('ticket_created', 'ticket_updated', 'ticket_resolved')
            ticket (Ticket): Instância do ticket
        """
        channel_layer = get_channel_layer()
        if channel_layer:
            ticket_data = TicketSerializer(ticket).data
            async_to_sync(channel_layer.group_send)(
                'ticket_notifications', {'type': notification_type, 'ticket': ticket_data}
            )

    @classmethod
    def send_ticket_created(cls, ticket):
        """Envia notificação de ticket criado"""
        cls.send_ticket_notification('ticket_created', ticket)

    @classmethod
    def send_ticket_updated(cls, ticket):
        """Envia notificação de ticket atualizado"""
        cls.send_ticket_notification('ticket_updated', ticket)

    @classmethod
    def send_ticket_resolved(cls, ticket):
        """Envia notificação de ticket resolvido"""
        cls.send_ticket_notification('ticket_resolved', ticket)

    @classmethod
    def send_custom_notification(cls, message, notification_type='info'):
        """
        Envia notificação customizada

        Args:
            message (str): Mensagem da notificação
            notification_type (str): Tipo da notificação ('info', 'success', 'warning', 'error')
        """
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                'ticket_notifications',
                {'type': 'custom_notification', 'message': message, 'notification_type': notification_type},
            )
