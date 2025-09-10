from django import template
from core.models import TicketStatus

register = template.Library()

@register.filter
def status_badge_class(status):
    """Map ticket status to Bootstrap badge class"""
    status_mapping = {
        TicketStatus.OPEN.value: 'success',
        TicketStatus.IN_PROGRESS.value: 'primary',
        TicketStatus.RESOLVED.value: 'info',
        TicketStatus.CANCELLED.value: 'danger',
    }
    return f"bg-{status_mapping.get(status, 'secondary')}"

@register.filter
def priority_badge_class(priority):
    """Map ticket priority to Bootstrap badge class"""
    priority_mapping = {
        'low': 'success',
        'medium': 'primary',
        'high': 'warning',
        'urgent': 'danger',
    }
    return f"bg-{priority_mapping.get(priority, 'secondary')}"
