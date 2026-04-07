from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import (
    AuditLog, Company, Brigade, Employee, Client,
    ConstructionObject, Contract, ConstructionStage,
    Material, MaterialUsage, Equipment, Payment
)

TRACKED_MODELS = [
    Company, Brigade, Employee, Client,
    ConstructionObject, Contract, ConstructionStage,
    Material, MaterialUsage, Equipment, Payment
]

def log_action(instance, action):
    AuditLog.objects.create(
        employee=None,
        action=action,
        table_name=instance.__class__.__name__,
    )

def register_signals():
    for model in TRACKED_MODELS:
        post_save.connect(
            lambda sender, instance, created, **kwargs: log_action(
                instance, 'CREATE' if created else 'UPDATE'
            ),
            sender=model,
            weak=False
        )
        post_delete.connect(
            lambda sender, instance, **kwargs: log_action(instance, 'DELETED'),
            sender=model,
            weak=False
        )
        