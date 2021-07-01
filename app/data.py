import numpy as np
import pandas as pd

from .snowflake import fetch_from_sql_file
from .logger import logger
from .settings import Settings

settings = Settings()

DATASETS_DIR = settings.file_system.datasets_path
DATASET_FNAME = settings.file_system.dataset_sql
MAX_NUM_RECORDS = settings.dataset.max_num_records
PRIMARY_KEY = settings.dataset.primary_key
DATA_PATH = settings.dataset.data_path


def load_dataset():

    # Fetch the dataset stored in row format.
    raw_data = _fetch_data(DATASET_FNAME, data_path=DATA_PATH, max_record_count=MAX_NUM_RECORDS)

    _validate_data(raw_data)

    _format_data(raw_data)

    data = _pivot_data(raw_data)

    return data


def _fetch_data(dataset_fname, **kwargs):
    logger.info(f"Fetching {dataset_fname}")
    raw_data = fetch_from_sql_file(dataset_fname, **kwargs)
    logger.info(f"Fetched {len(raw_data):,.0f} records")
    return raw_data


def _format_data(raw_data):
    logger.info("Ensuring data is correctly formatted")

    # Make sure fields have the right data type
    raw_data['latitude'] = raw_data.latitude.astype(float)
    raw_data['longitude'] = raw_data.longitude.astype(float)
    raw_data['max_travel_distance_meters'] = raw_data.max_travel_distance_meters.astype(float)


def _validate_data(raw_data):
    logger.info("Verifying data is as expected")

    num_records = len(raw_data)

    # No need for tests if we return a dataset with no rows in it.
    if num_records > 0:

        # Make sure there are no duplicate rows
        unique_key = [PRIMARY_KEY]

        num_unique_records = len(raw_data[unique_key].drop_duplicates())
        if num_records != num_unique_records:
            raise Exception("Some records were duplicates.")

    logger.info("Tests pass")


def _pivot_data(raw_data):

    logger.info("Pivoting dataset")
    
    data = raw_data # Nothing to do

    logger.info(f"Pivoted the data into {len(data):,.0f} records")

    return data

