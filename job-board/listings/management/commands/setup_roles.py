# listings/management/commands/setup_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from listings.models import Job, Category

class Command(BaseCommand):
    help = "Create default groups and permissions"

    def handle(self, *args, **kwargs):
        admins, _ = Group.objects.get_or_create(name="Admins")
        users, _ = Group.objects.get_or_create(name="Users")

        # Give admins all permissions for Job and Category
        for model in [Job, Category]:
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=ct)
            for p in perms:
                admins.permissions.add(p)

        self.stdout.write(self.style.SUCCESS("Roles and permissions setup complete."))
