from rest_framework import serializers
from core.models import Ticket, CustomUser, TicketStatus


class UserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'role', 'department']
        read_only_fields = ['id']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket"""
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'priority', 'priority_display',
            'department', 'status', 'status_display', 'created_by', 
            'assigned_to', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class TicketCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tickets"""
    
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'department']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['status'] = TicketStatus.OPEN.value
        return super().create(validated_data)


class TicketUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating tickets"""
    
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'department', 'status']
    
    def validate_status(self, value):
        """Validate status changes"""
        ticket = self.instance
        if ticket and ticket.status in TicketStatus.get_non_editable_statuses():
            raise serializers.ValidationError("Cannot edit closed or cancelled tickets.")
        return value
    
class HealthCheckSerializer(serializers.Serializer):
    """Serializer for health check response"""
    status = serializers.CharField()
    message = serializers.CharField()
    version = serializers.CharField()


class ApiInfoSerializer(serializers.Serializer):
    """Serializer for API info response"""
    name = serializers.CharField()
    version = serializers.CharField()
    description = serializers.CharField()
    endpoints = serializers.DictField()
    authentication = serializers.DictField()