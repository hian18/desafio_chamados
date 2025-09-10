from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.translation import gettext as _

from services import websocket_service 
from core.models import Ticket, TicketStatus


def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('front:dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, _('Welcome, %(name)s!') % {'name': user.get_full_name()})
            return redirect('front:dashboard')
        else:
            messages.error(request, _('Invalid email or password.'))

    return render(request, 'front/login.html')


@login_required
def logout_view(request):
    """Logout user"""
    logout(request)
    messages.info(request, _('You have been logged out.'))
    return redirect('front:login')


@login_required
def dashboard_view(request):
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    search_query = request.GET.get('search', '')
    # Base queryset
    tickets = Ticket.objects.select_related('created_by').all()
    # Apply filters
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)
    if search_query:
        tickets = tickets.filter(title__icontains=search_query)
    # Pagination
    paginator = Paginator(tickets, 10)  # 10 tickets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Get choices for filters
    status_choices = TicketStatus.get_choices()
    priority_choices = Ticket.PRIORITY_CHOICES

    context = {
        'page_obj': page_obj,
        'status_choices': status_choices,
        'priority_choices': priority_choices,
        'current_status': status_filter,
        'current_priority': priority_filter,
        'search_query': search_query,
    }
    return render(request, 'front/dashboard.html', context)


@login_required
def ticket_detail_view(request, ticket_id):
    """Ticket detail view"""
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        messages.error(request, 'Ticket not found.')
        return redirect('front:dashboard')
    context = {
        'ticket': ticket,
        'non_editable_statuses': TicketStatus.get_non_editable_statuses(),
    }
    return render(request, 'front/ticket_detail.html', context)


@login_required
def create_ticket_view(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        priority = request.POST.get('priority', '').strip()
        department = request.POST.get('department', '').strip()

        # Validate required fields
        if not title:
            messages.error(request, 'Title is required.')
            return redirect('front:dashboard')
        if not description:
            messages.error(request, 'Description is required.')
            return redirect('front:dashboard')
        if not priority:
            messages.error(request, 'Priority is required.')
            return redirect('front:dashboard')

        try:
            ticket = Ticket.objects.create(
                title=title,
                description=description,
                priority=priority,
                status=TicketStatus.OPEN.value,  # Always set to open for new tickets
                department=department,
                created_by=request.user,
            )
            websocket_service.send_ticket_created(ticket)
            messages.success(request, f'Ticket #{ticket.id} created successfully!')
            return redirect('front:ticket_detail', ticket_id=ticket.id)
        except Exception as e:
            messages.error(request, f'Error creating ticket: {str(e)}')
            print(f"ERROR: {str(e)}")
            return redirect('front:dashboard')

    return redirect('front:dashboard')


@login_required
def edit_ticket_view(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        messages.error(request, _('Ticket not found.'))
        return redirect('front:dashboard')

    # Check if ticket is closed or cancelled (cannot be edited)
    if ticket.status in TicketStatus.get_non_editable_statuses():
        messages.error(request, _('Cannot edit closed or cancelled tickets.'))
        return redirect('front:ticket_detail', ticket_id=ticket.id)

    # Check permissions (only creator or assigned user can edit)
    if ticket.created_by != request.user and ticket.assigned_to != request.user and not request.user.is_superuser:
        messages.error(request, _('You do not have permission to edit this ticket.'))
        return redirect('front:ticket_detail', ticket_id=ticket.id)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        priority = request.POST.get('priority', '').strip()
        status = request.POST.get('status', '').strip()
        department = request.POST.get('department', '').strip()

        # Validate required fields
        if not title:
            messages.error(request, _('Title is required.'))
            return redirect('front:edit_ticket', ticket_id=ticket.id)
        if not description:
            messages.error(request, _('Description is required.'))
            return redirect('front:edit_ticket', ticket_id=ticket.id)
        if not priority:
            messages.error(request, _('Priority is required.'))
            return redirect('front:edit_ticket', ticket_id=ticket.id)
        if not status:
            messages.error(request, _('Status is required.'))
            return redirect('front:edit_ticket', ticket_id=ticket.id)

        try:
            # Update ticket
            ticket.title = title
            ticket.description = description
            ticket.priority = priority
            ticket.status = status
            ticket.department = department
            ticket.updated_by = request.user
            ticket.save()

            messages.success(request, _('Ticket #%(id)s updated successfully!') % {'id': ticket.id})
            return redirect('front:ticket_detail', ticket_id=ticket.id)
        except Exception as e:
            messages.error(request, _('Error updating ticket: %(error)s') % {'error': str(e)})
            return redirect('front:edit_ticket', ticket_id=ticket.id)

    status_choices = TicketStatus.get_editable_choices()
    priority_choices = Ticket.PRIORITY_CHOICES

    context = {
        'ticket': ticket,
        'status_choices': status_choices,
        'priority_choices': priority_choices,
    }

    return render(request, 'front/edit_ticket.html', context)
