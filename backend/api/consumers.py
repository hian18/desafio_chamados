import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from core.models import Ticket


class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'ticket_notifications'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'ticket_notification',
                'message': message
            }
        )

    # Receive message from room group
    async def ticket_notification(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message
        }))

    # Receive ticket created notification
    async def ticket_created(self, event):
        ticket_data = event['ticket']
        
        await self.send(text_data=json.dumps({
            'type': 'ticket_created',
            'ticket': ticket_data
        }))

    # Receive ticket updated notification
    async def ticket_updated(self, event):
        ticket_data = event['ticket']
        
        await self.send(text_data=json.dumps({
            'type': 'ticket_updated',
            'ticket': ticket_data
        }))

    # Receive ticket resolved notification
    async def ticket_resolved(self, event):
        ticket_data = event['ticket']
        
        await self.send(text_data=json.dumps({
            'type': 'ticket_resolved',
            'ticket': ticket_data
        }))

    # Receive custom notification
    async def custom_notification(self, event):
        message = event['message']
        notification_type = event.get('notification_type', 'info')
        await self.send(text_data=json.dumps({
            'type': 'custom_notification',
            'message': message,
            'notification_type': notification_type
        }))
