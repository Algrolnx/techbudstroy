from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import (
    Company, Brigade, Employee, Client,
    ConstructionObject, Contract, ConstructionStage,
    Material, MaterialUsage, Equipment, Payment, AuditLog
)


class Command(BaseCommand):
    help = 'Створює групи ролей: Менеджер, Бухгалтер, Читач'

    def handle(self, *args, **kwargs):
        all_models = [
            Company, Brigade, Employee, Client,
            ConstructionObject, Contract, ConstructionStage,
            Material, MaterialUsage, Equipment, Payment, AuditLog
        ]

        view_perms = []
        change_perms = []
        add_perms = []

        for model in all_models:
            ct = ContentType.objects.get_for_model(model)
            view_perms += list(Permission.objects.filter(content_type=ct, codename__startswith='view_'))
            add_perms += list(Permission.objects.filter(content_type=ct, codename__startswith='add_'))
            change_perms += list(Permission.objects.filter(content_type=ct, codename__startswith='change_'))

        manager_group, created = Group.objects.get_or_create(name='Менеджер')
        manager_group.permissions.set(
            view_perms + add_perms + change_perms
        )
        self.stdout.write(self.style.SUCCESS(
            f'{"Створено" if created else "Оновлено"} групу: Менеджер'
        ))

        accountant_models = [Contract, Payment, Client]
        accountant_perms = []
        for model in accountant_models:
            ct = ContentType.objects.get_for_model(model)
            accountant_perms += list(Permission.objects.filter(content_type=ct))

        accountant_group, created = Group.objects.get_or_create(name='Бухгалтер')
        accountant_group.permissions.set(accountant_perms)
        self.stdout.write(self.style.SUCCESS(
            f'{"Створено" if created else "Оновлено"} групу: Бухгалтер'
        ))

        reader_group, created = Group.objects.get_or_create(name='Читач')
        reader_group.permissions.set(view_perms)
        self.stdout.write(self.style.SUCCESS(
            f'{"Створено" if created else "Оновлено"} групу: Читач'
        ))
