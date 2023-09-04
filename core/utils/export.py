from typing import Dict, List
from core.models import InjestedTextContent, ContentPool, ProcessedData
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict


def get_data_dump(
    queryset: QuerySet[InjestedTextContent], content_pool: ContentPool
) -> List[Dict]:
    injested_text_contents = queryset.filter(process_completed_successfully=True)

    processed_data: QuerySet[ProcessedData] = ProcessedData.objects.filter(
        content_pool=content_pool, injested_text_content__in=injested_text_contents
    ).prefetch_related("prompt", "injested_text_content")

    processed_content_dict = {}

    for data in processed_data:
        if data.injested_text_content_id in processed_content_dict:
            processed_content_dict[data.injested_text_content_id][
                data.prompt.prompt_name
            ] = data.prompt_result
        else:
            processed_content_dict[data.injested_text_content_id] = {
                "content_uuid": data.injested_text_content.content_uuid,
                "content_pool_name": data.injested_text_content.content_pool.pool_name,
                "text_content": data.injested_text_content.text_content,
                "metadata_json": data.injested_text_content.metadata_json,
                "datasource_name": data.injested_text_content.datasource.datasource_name,
                "processed_at": data.injested_text_content.processed_at,
            }

            processed_content_dict[data.injested_text_content_id][
                data.prompt.prompt_name
            ] = data.prompt_result

    return list(processed_content_dict.values)
