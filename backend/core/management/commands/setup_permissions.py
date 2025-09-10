from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import CustomUser, Ticket


class Command(BaseCommand):
    help = 'Setup user groups and permissions for the ticket system'

    def handle(self, *args, **options):
        # Create groups
        groups_data = {
            'Administrators': {
                'permissions': [
                    'can_view_tickets', 'can_create_tickets', 'can_edit_tickets',
                    'can_delete_tickets', 'can_assign_tickets', 'can_close_tickets',
                    'can_view_reports', 'can_manage_users'
                ],
                'description': 'Full access to all features'
            },
            'Managers': {
                'permissions': [
                    'can_view_tickets', 'can_create_tickets', 'can_edit_tickets',
                    'can_assign_tickets', 'can_close_tickets', 'can_view_reports'
                ],
                'description': 'Can manage tickets and view reports'
            },
            'Agents': {
                'permissions': [
                    'can_view_tickets', 'can_create_tickets', 'can_edit_tickets',
                    'can_close_tickets'
                ],
                'description': 'Can work with tickets assigned to them'
            },
            'Users': {
                'permissions': [
                    'can_view_tickets', 'can_create_tickets'
                ],
                'description': 'Can view and create tickets'
            }
        }

        # Create groups and assign permissions
        for group_name, group_data in groups_data.items():
            group, created = Group.objects.get_or_create(name=group_name)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created group: {group_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Group already exists: {group_name}')
                )

            # Clear existing permissions
            group.permissions.clear()

            # Add permissions
            for perm_codename in group_data['permissions']:
                try:
                    permission = Permission.objects.get(
                        codename=perm_codename,
                        content_type__app_label='core'
                    )
                    group.permissions.add(permission)
                    self.stdout.write(
                        f'  Added permission: {permission.name}'
                    )
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'  Permission not found: {perm_codename}')
                    )

        # Create default admin user if it doesn't exist
        if not CustomUser.objects.filter(username='admin').exists():
            admin_user = CustomUser.objects.create_superuser(
                username='admin',
                email='admin@openticket.com',
                password='admin123',
                role='admin',
                first_name='System',
                last_name='Administrator'
            )
            admin_group = Group.objects.get(name='Administrators')
            admin_user.groups.add(admin_group)
            
            self.stdout.write(
                self.style.SUCCESS('Created default admin user: admin/admin123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Admin user already exists')
            )

        self.stdout.write(
            self.style.SUCCESS('Permission setup completed successfully!')
        )
