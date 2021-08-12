import errno
from typing import Any, Dict
import numpy as np
from os import path, strerror
import pandas as pd

from app.snowflake import fetch_from_sql_file
from app.logger import logger
from app.settings import Settings

settings = Settings()

DATASETS_DIR = settings.file_system.datasets_path

class Dataset():
    def __init__(self, fname: str, sql_interpolations: Dict[str,Any]) -> None:

        dataset_path = path.join(DATASETS_DIR, fname)

        if not path.isfile(dataset_path):
            raise(errno.ENOENT, strerror(errno.ENOENT), dataset_path)

        self.fname = fname
        self.dataset_path = dataset_path
        self.sql_interpolations = sql_interpolations


    def load_dataset(self):
        # Fetch the dataset stored in row format.
        logger.info(f"Fetching data according to {self.fname}")
        raw_data = self._fetch_raw_data()
        logger.info(f"Fetched {len(raw_data):,.0f} records")

        logger.info("Verifying data is as expected")
        self._validate_data(raw_data)

        logger.info("Ensuring data is correctly formatted")
        self._format_data(raw_data)

        logger.info("Pivoting dataset")
        data = self._pivot_data(raw_data)
        logger.info(f"Pivoted the data into {len(data):,.0f} records")

        return data


    def _fetch_raw_data(self):
        return fetch_from_sql_file(self.dataset_path, **self.sql_interpolations)

    # Override these as required

    def _format_data(self, raw_data):
        pass

    def _validate_data(self, raw_data):
        pass

    def _pivot_data(self, raw_data):
        return raw_data # Nothing to do

