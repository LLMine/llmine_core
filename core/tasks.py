import csv
import io
import tempfile
import uuid
from celery import shared_task

from core.utils.export import get_data_dump
from .models import (
    ExtracterChain,
    InjestedTextContent,
    ExtracterPrompt,
    ProcessedData,
    ContentPool,
    DataExport,
)
from .utils.llm_service import get_llm_service
from django.utils import timezone
from django.template import Context, Template
from django.db.models.query import QuerySet

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import jinja2


def should_run_prompt(run_if_expr, prompt_response_map):
    if run_if_expr is None or run_if_expr.strip() == "":
        return True

    environment = jinja2.Environment()
    template_str = "{% if " + run_if_expr + " %} True {% else %} False {% endif %}"
    template = environment.from_string(template_str)
    bool_str = template.render(prompt_response_map).strip()

    return bool_str == "True"


def run_extracter_chain(
    extracter_chain,
    content_pool,
    injested_text_content: InjestedTextContent,
    content_uuid,
):
    extracter_prompts = ExtracterPrompt.objects.filter(
        extracter_chain=extracter_chain
    ).order_by("order_index")

    if not extracter_prompts.exists():
        print(
            f"Prompts not configured for text_content with UUID: {content_uuid} -- Content Pool: {content_pool} -- Extracter Chain: {extracter_chain}"
        )
        return

    llm_service = get_llm_service(extracter_chain.llm_name)
    llm_service.init_chain()

    prompt_response_map = {}

    for extracter_prompt in extracter_prompts:
        if not should_run_prompt(extracter_prompt.run_if_expr, prompt_response_map):
            prompt_response_map[
                extracter_prompt.prompt_name
            ] = "x_llmine_skipped_execution"
            continue

        step_response = llm_service.process_prompt(
            injested_text_content.text_content,
            extracter_prompt.prompt_text,
            extracter_prompt.return_type,
            extracter_prompt.jsonschema,
            extracter_prompt.labels_config_json,
        )

        prompt_response_map[extracter_prompt.prompt_name] = step_response

        # TODO: Validate step_response based on return type

        ProcessedData.objects.create(
            content_pool=content_pool,
            injested_text_content=injested_text_content,
            chain=extracter_chain,
            prompt=extracter_prompt,
            prompt_result=step_response,
        )

    return True


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 1},
    task_time_limit=600,
)
def process_ingested_content(self, content_uuid):
    # Fetch the prompts configured for the given content_uuid
    ingested_text_content = InjestedTextContent.objects.get(content_uuid=content_uuid)

    if ingested_text_content.process_completed_successfully:
        return

    content_pool = ingested_text_content.content_pool
    extracter_chains = ExtracterChain.objects.filter(content_pool=content_pool)

    success = True
    for extracter_chain in extracter_chains:
        chain_success = run_extracter_chain(
            extracter_chain, content_pool, ingested_text_content, content_uuid
        )

        success = success and chain_success

    ingested_text_content.processed_at = timezone.now()
    ingested_text_content.process_completed_successfully = success

    ingested_text_content.save()


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 1},
    task_time_limit=600,
)
def process_data_export(self, exported_ingestable_content_ids, content_pool_id):
    """
    Current implementation needs the entire data in memory. It also writes the CSV to an in-mem buffer.
    This is not ideal and not scalable. It might lead to high memory usage for large datasets.

    TODO: Refactor the logic to stream from DB, transform and immediately flush to file.
    """
    export_uuid = uuid.uuid4()

    queryset: QuerySet[InjestedTextContent] = InjestedTextContent.objects.filter(
        id__in=exported_ingestable_content_ids
    )
    content_pool = ContentPool.objects.get(id=content_pool_id)

    data, headers = get_data_dump(queryset, content_pool)
    if not len(data) > 0:
        return

    print(data)
    print(headers)

    buffer = io.StringIO()

    writer = csv.DictWriter(buffer, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

    buffer.seek(0)
    saved_path = default_storage.save(
        f"exported_data/{export_uuid}.csv", ContentFile(buffer.read())
    )

    buffer.close()

    DataExport.objects.create(
        export_uuid=export_uuid,
        export_type="Processed Content",
        data_file=saved_path,
    )
