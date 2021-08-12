from app.settings import Settings
from .dataset import Dataset

settings = Settings()

DATASET_FNAME = "unique_locations_48h.sql"

SQL_INTERPOLATIONS = {
    "max_record_count": settings.dataset.max_num_records,
    "data_path": settings.dataset.main_data_path,
    "event_source": "PROD.RAW.AIRTASKER_EVENT",
    "event_name": 'Discovery Page View',
}

class UniqueLocationsDataset48h(Dataset):
    def __init__(self) -> None:
        super().__init__(DATASET_FNAME, SQL_INTERPOLATIONS)

    def _format_data(self, raw_data):
        # Make sure fields have the right data type
        raw_data['latitude'] = raw_data.latitude.astype(float)
        raw_data['longitude'] = raw_data.longitude.astype(float)
