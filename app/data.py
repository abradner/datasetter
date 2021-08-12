import errno
import numpy as np
from os import path, strerror
import pandas as pd

from .snowflake import fetch_from_sql_file
from .logger import logger
from .settings import Settings
from .datasets.listing_locations import ListingsLocationsDataset
settings = Settings()

DATASETS_DIR = settings.file_system.datasets_path
DATASET_FNAME = "dataset.sql"
MAX_NUM_RECORDS = settings.dataset.max_num_records
PRIMARY_KEY = settings.dataset.primary_key
DATA_SOURCE_PATH = settings.dataset.data_path

def load_dataset(fname = DATASET_FNAME):
    
