from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum


class TicketStatus(Enum):
    """Enum for ticket statuses"""

    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    RESOLVED = 'resolved'
    CANCELLED = 'cancelad'

    @classmethod
    def get_non_editable_statuses(cls):
        """Returns statuses that cannot be edited"""
        return [cls.RESOLVED, cls.CANCELLED.value]

    @classmethod
    def get_editable_choices(cls):
        """Returns only editable status choices (without resolved and closed)"""
        return [
            (cls.OPEN.value, 'Open'),
            (cls.IN_PROGRESS.value, 'In Progress'),
            (cls.CANCELLED.value, 'Cancelled'),
        ]

    @classmethod
    def get_choices(cls):
        """Returns choices for Django model field"""
        return [
            (cls.OPEN.value, 'Open'),
            (cls.IN_PROGRESS.value, 'In Progress'),
            (cls.RESOLVED.value, 'Resolved'),
            (cls.CANCELLED.value, 'Cancelled'),
        ]


class CustomUser(AbstractUser):
    """Custom user model with additional fields"""

    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('technician', 'Technician'),
        ('agent', 'Agent'),
    ]

    email = models.EmailField(unique=True, verbose_name='Email')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name='Role')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Phone')
    department = models.CharField(max_length=50, blank=True, verbose_name='Department')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        permissions = [
            ('can_view_tickets', 'Can view tickets'),
            ('can_create_tickets', 'Can create tickets'),
            ('can_edit_tickets', 'Can edit tickets'),
            ('can_delete_tickets', 'Can delete tickets'),
            ('can_assign_tickets', 'Can assign tickets'),
            ('can_close_tickets', 'Can close tickets'),
            ('can_view_reports', 'Can view reports'),
            ('can_manage_users', 'Can manage users'),
        ]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def has_ticket_permission(self, permission):
        """Check if user has specific ticket permission"""
        return self.has_perm(f'core.{permission}') or self.is_superuser

    def is_ticket_manager(self):
        """Check if user can manage tickets"""
        return self.role in ['admin', 'manager'] or self.is_superuser

    def is_ticket_agent(self):
        """Check if user can work with tickets"""
        return self.role in ['admin', 'manager', 'agent'] or self.is_superuser


class BaseModel(models.Model):
    """Base model with audit fields"""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Deleted At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated',
        verbose_name='Updated By',
    )

    class Meta:
        abstract = True


class Ticket(BaseModel):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=200, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name='Priority')
    department = models.CharField(max_length=20, verbose_name='Department')
    status = models.CharField(
        max_length=20, choices=TicketStatus.get_choices(), default=TicketStatus.OPEN.value, verbose_name='Status'
    )
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='created_tickets', verbose_name='Created By'
    )
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets',
        verbose_name='Assigned To',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
