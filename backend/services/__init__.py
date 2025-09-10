from .websocket_service import WebSocketNotificationService
from .notification_service import NotificationService

# Instâncias globais dos serviços
websocket_service = WebSocketNotificationService()
notification_service = NotificationService()

__all__ = [
    'WebSocketNotificationService',
    'NotificationService',
    'websocket_service',
    'notification_service'
]
