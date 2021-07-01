from .algolia_client import Client as AlgoliaClient
import pandas as pd
from .logger import logger

def prepare_dataset_for_algolia(df: pd.DataFrame) -> dict:
    dfc = df.rename(columns={"id": "objectID",}) # make a copy
    dfc[['created_at', 'updated_at']] = dfc[['created_at', 'updated_at']].apply(pd.to_numeric)
    return dfc.to_dict(orient="records")


def configure_algolia_index(client: AlgoliaClient) -> None:
    facet_attributes = [
        'geohashes',
        'max_lat',
        'min_lat',
        'max_lon',
        'min_lon'
    ]
    
    filter_attributes = list(map(lambda el: f"filterOnly({el})", facet_attributes))
    
    return client.set_facets(filter_attributes)


def add_data_to_algolia(client: AlgoliaClient, df: pd.DataFrame) -> None:
    logger.info("Adding data to algolia")
    data = prepare_dataset_for_algolia(df)
    configure_algolia_index(client)
    client.push(data)
