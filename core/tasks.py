from celery import shared_task
from .models import InjestedTextContent, ExtracterPrompt
from .utils.llm_service import get_llm_service
from .utils.prompting import get_user_content


def get_prompt_output():
    pass

def run_extracter_chain(extracter_chain, content_pool, injested_text_content, llm_name):
    extracter_prompts = ExtracterPrompt.objects.filter(extracter_chain=extracter_chain)

    if not extracter_prompts.exists():
        print(f"Prompts not configured for text_content with UUID: {content_uuid} -- Content Pool: {content_pool} -- Extracter Chain: {extracter_chain}")
        return
    
    try:
        llm_service = get_llm_service(llm_name)

        messages = [llm_service.get_system_prompt()]
        
        for extracter_prompt in extracter_prompts:
            messages.add(get_user_content(llm_name, extracter_prompt))
            llm_response = llm_service.fetch_response(messages)
            messages.add(get_assistant_prompt(llm_name, extracter_prompt))
            # Construct a processvalue obj and save it to db.


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
    content_pool = ingested_text_content.content_pool
    llm_name = content_pool.llm_name
    extracter_chains = ExtracterChain.objects.filter(content_pool=content_pool)
    
    for extracter_chain in extracter_chains:
        run_extracter_chain(extracter_chain, content_pool, ingested_text_content, llm_name)


    





    


    



