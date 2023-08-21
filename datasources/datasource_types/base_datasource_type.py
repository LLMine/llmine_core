from abc import ABC, abstractmethod
from typing import Dict


class IngestableData:
    def __init__(self, content_pool=None, text_content="", metadata_json=None):
        self.content_pool = (
            content_pool  # This should be an instance of ContentPool or similar
        )
        self.text_content = text_content
        self.metadata_json = metadata_json if metadata_json is not None else {}

    def __str__(self):
        return f"Content Pool: {self.content_pool}, Text Content: {self.text_content}, Metadata JSON: {self.metadata_json}"


class BaseDataSourceType(ABC):
    @abstractmethod
    def transform(self, data_sent_from_source: Dict) -> IngestableData:
        pass
