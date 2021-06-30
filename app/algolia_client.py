from algoliasearch.search_client import SearchClient
from .settings import Settings
import pandas as pd

class Client():
    def __init__(self) -> None:
        settings = Settings().algolia
        self.client = SearchClient.create(settings.app_id, settings.admin_api_key)
        self.index = self.client.init_index(settings.index)
        self.settings = settings

    def push(self, data: list):
        self.index.clear_objects()

        trimmed_data = data[:self.settings.max_records]
        return self.index.save_objects(trimmed_data, {'autoGenerateObjectIDIfNotExist': False})


    def set_facets(self, attributes: list):
        return self.index.set_settings({
            'attributesForFaceting': attributes
        })

    def query(self, query_string: str = '', filters: str = '', numeric_filters: list = []):
        return self.index.search(query_string, {
            'filters': filters,
            "numericFilters": numeric_filters
        })
