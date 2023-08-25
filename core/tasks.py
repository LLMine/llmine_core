from celery import shared_task
from .models import ExtracterChain, InjestedTextContent, ExtracterPrompt, ProcessedData
from .utils.llm_service import get_llm_service
from django.utils import timezone
from django.template import Context, Template

import jinja2


def should_run_prompt(run_if_expr, prompt_response_map):
    if run_if_expr is None:
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
    llm_name,
):
    extracter_prompts = ExtracterPrompt.objects.filter(
        extracter_chain=extracter_chain
    ).order_by("order_index")

    if not extracter_prompts.exists():
        print(
            f"Prompts not configured for text_content with UUID: {content_uuid} -- Content Pool: {content_pool} -- Extracter Chain: {extracter_chain}"
        )
        return

    llm_service = get_llm_service(llm_name)
    llm_service.init_chain()

    prompt_response_map = {}

    for extracter_prompt in extracter_prompts:
        if not should_run_prompt(extracter_prompt.run_if_expr):
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
    llm_name = content_pool.llm_name
    extracter_chains = ExtracterChain.objects.filter(content_pool=content_pool)

    success = True
    for extracter_chain in extracter_chains:
        chain_success = run_extracter_chain(
            extracter_chain, content_pool, ingested_text_content, content_uuid, llm_name
        )

        success = success and chain_success

    ingested_text_content.processed_at = timezone.now()
    ingested_text_content.process_completed_successfully = success

    ingested_text_content.save()
