from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Set up groups and assign custom permissions for the Book model.'

    def handle(self, *args, **options):
        # Define group names and their permissions
        group_permissions = {
            'Editors': ['can_create', 'can_edit'],
            'Viewers': ['can_view'],
            'Admins': ['can_create', 'can_edit', 'can_delete', 'can_view'],
        }

        for group_name, perms in group_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_codename in perms:
                try:
                    perm = Permission.objects.get(codename=perm_codename, content_type__app_label='bookshelf')
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permission {perm_codename} not found.'))
            group.save()
            self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" updated with permissions: {perms}'))

        self.stdout.write(self.style.SUCCESS('Groups and permissions setup complete.')) 