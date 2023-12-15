from django.db.models.signals import post_save
from django.dispatch import receiver

from .etl import DomainETL
from .models import Domain


@receiver(post_save, sender=Domain)
def domain_etl(sender, instance, **kwargs):  # noqa
    DomainETL.run(domain_id=instance.id)
