from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models
from drf_spectacular.utils import extend_schema, extend_schema_view
from core.models import Ticket, TicketStatus
from .serializers import (
    ApiInfoSerializer,
    HealthCheckSerializer,
    TicketSerializer,
    TicketCreateSerializer,
    TicketUpdateSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes


@extend_schema(
    tags=['Health'],
    summary='Health Check',
    description='Verifica se a API v1 está funcionando',
    responses={200: OpenApiResponse(response=HealthCheckSerializer, description='API funcionando normalmente')},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint for API v1"""
    return Response({'status': 'ok', 'message': 'API v1 is running', 'version': '1.0.0'})


@extend_schema(
    tags=['API v1'],
    summary='API Information',
    description='Informações sobre a API v1',
    responses={200: OpenApiResponse(response=ApiInfoSerializer, description='Informações da API')},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """API information endpoint"""
    return Response(
        {
            'name': 'OpenTicket API',
            'version': '1.0.0',
            'description': 'Sistema de tickets - API v1',
            'endpoints': {
                'health': '/api/v1/health/',
                'info': '/api/v1/info/',
                'docs': '/api/docs/',
                'schema': '/api/schema/',
            },
            'authentication': {
                'type': 'JWT',
                'login': '/api/token/',
                'refresh': '/api/token/refresh/',
                'verify': '/api/token/verify/',
            },
        }
    )


@extend_schema_view(
    list=extend_schema(summary="List tickets", description="Get a list of all tickets with filtering and pagination"),
    retrieve=extend_schema(
        summary="Get ticket details", description="Get detailed information about a specific ticket"
    ),
    create=extend_schema(summary="Create ticket", description="Create a new ticket"),
    update=extend_schema(summary="Update ticket", description="Update an existing ticket"),
    partial_update=extend_schema(summary="Partially update ticket", description="Partially update an existing ticket"),
    destroy=extend_schema(summary="Delete ticket", description="Delete a ticket (soft delete)"),
)
class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tickets
    """

    queryset = Ticket.objects.select_related('created_by', 'assigned_to').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'department']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'priority']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return TicketCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TicketUpdateSerializer
        return TicketSerializer

    def get_queryset(self):
        """Filter tickets based on user permissions"""
        queryset = super().get_queryset()
        user = self.request.user

        # If user is not superuser, filter by created_by or assigned_to
        if not user.is_superuser:
            queryset = queryset.filter(models.Q(created_by=user) | models.Q(assigned_to=user))

        return queryset

    def perform_create(self, serializer):
        """Set the created_by field to the current user"""
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """Set the updated_by field to the current user"""
        serializer.save(updated_by=self.request.user)

    @extend_schema(summary="Mark ticket as resolved", description="Mark a ticket as resolved")
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Mark ticket as resolved"""
        ticket = self.get_object()

        # Check if ticket can be resolved
        if ticket.status in TicketStatus.get_non_editable_statuses():
            return Response(
                {'error': 'Cannot resolve closed or cancelled tickets.'}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check permissions
        if ticket.created_by != request.user and ticket.assigned_to != request.user and not request.user.is_superuser:
            return Response(
                {'error': 'You do not have permission to resolve this ticket.'}, status=status.HTTP_403_FORBIDDEN
            )

        # Update ticket status
        ticket.status = TicketStatus.RESOLVED.value
        ticket.updated_by = request.user
        ticket.save()

        serializer = self.get_serializer(ticket)
        return Response(serializer.data)

    @extend_schema(summary="Get ticket statistics", description="Get statistics about tickets")
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get ticket statistics"""
        queryset = self.get_queryset()

        stats = {
            'total': queryset.count(),
            'open': queryset.filter(status=TicketStatus.OPEN.value).count(),
            'in_progress': queryset.filter(status=TicketStatus.IN_PROGRESS.value).count(),
            'pending': queryset.filter(status=TicketStatus.PENDING.value).count(),
            'resolved': queryset.filter(status=TicketStatus.RESOLVED.value).count(),
            'cancelled': queryset.filter(status=TicketStatus.CANCELLED.value).count(),
        }

        return Response(stats)
