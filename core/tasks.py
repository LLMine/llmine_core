from celery import shared_task
from .models import InjestedTextContent, ExtracterPrompt


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 1},
    task_time_limit=600,
)
def process_ingested_content(self, content_uuid):
    pass
