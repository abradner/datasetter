from .algolia_benchmark import benchmark_searches
from .algolia_client import Client as AlgoliaClient
from .algolia_functions import add_data_to_algolia
from .boundaries_functions import calculate_boundaries
from .data import DATASETS_DIR, load_dataset
from .geohash_functions import create_geohash
from .gis_functions import Point
from .logger import logger
from .settings import Settings

import os
import pandas as pd

settings = Settings()

RAW_DATASET_FILE = os.path.join(DATASETS_DIR, "raw_dataset.pkl")
PROCESSED_DATASET_FILE = os.path.join(DATASETS_DIR, f"processed_dataset_precision_{settings.geohash_precision}.pkl")


def boundary_helper(row) -> pd.Series:
    data = calculate_boundaries(
            Point(row['latitude'], row['longitude']),
            row['max_travel_distance_meters']
        )
    return pd.Series(data=data, index=data.keys())


def add_boundaries(df: pd.DataFrame) -> None:
    logger.info("Calculating boundaries")
    df[
        ['max_lat', 'min_lat', 'max_lon', 'min_lon']
    ] = df[['latitude','longitude','max_travel_distance_meters']].apply(
        lambda row: boundary_helper(row), axis=1
    )

def add_geohashes(df: pd.DataFrame) -> None:
    logger.info("Calculating geohashes")
    df['geohashes'] = df[['latitude','longitude','max_travel_distance_meters']].apply(
        lambda row: create_geohash(
            float(row['latitude']),
            float(row['longitude']),
            row['max_travel_distance_meters'],
            settings.geohash_precision
        )
    , axis=1)


def prepare_records() -> pd.DataFrame:
    if os.path.isfile(PROCESSED_DATASET_FILE):
        logger.info('Processed Datafile already exists, loading file...')
        df = pd.read_pickle(PROCESSED_DATASET_FILE)
    else:
        if os.path.isfile(RAW_DATASET_FILE):
            logger.info('Raw Datafile already exists, loading file...')
            df = pd.read_pickle(RAW_DATASET_FILE)
        else:
            df = load_dataset()

            logger.info(f"saving {RAW_DATASET_FILE}")
            df.to_pickle(RAW_DATASET_FILE)

        add_boundaries(df)
        add_geohashes(df)

        logger.info(f"saving {PROCESSED_DATASET_FILE}")
        # save datafile
        df.to_pickle(PROCESSED_DATASET_FILE)
    return df


def index_records(algolia_client: AlgoliaClient) -> None:
    df = prepare_records()
    add_data_to_algolia(algolia_client, df)
    del df


def run(skip_indexing: bool = False) -> None:
    logger.info('Running')
    algolia_client = AlgoliaClient()

    if skip_indexing:
        pass
    else:
        index_records(algolia_client)

    benchmark_searches(algolia_client)


