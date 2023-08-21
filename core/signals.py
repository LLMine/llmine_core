from django.dispatch import receiver
from django.db.models.signals import post_save

from llmine_core import settings
from .models import *
from .tasks import process_ingested_content


@receiver(
    post_save,
    sender=InjestedTextContent,
    dispatch_uid="schedule_content_processing_task",
)
def schedule_content_processing_task(
    sender, instance: InjestedTextContent, created, **kwargs
):
    if created or settings.DEBUG:
        print(f"Scheduling processing task for ${instance.content_uuid}")
        process_ingested_content.delay(instance.content_uuid)
