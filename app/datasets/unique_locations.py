from app.settings import Settings
from .dataset import Dataset

settings = Settings()

PRIMARY_KEY = settings.dataset.primary_key

DATASET_FNAME = "unique_locations.sql"

SQL_INTERPOLATIONS = {
    "max_record_count": settings.dataset.max_num_records,
    "data_path": settings.dataset.main_data_path,
}

class UniqueLocationsDataset(Dataset):
    def __init__(self) -> None:
        super().__init__(DATASET_FNAME, SQL_INTERPOLATIONS)

    def _format_data(self, raw_data):
        # Make sure fields have the right data type
        raw_data['lat'] = raw_data.lat.astype(float)
        raw_data['lon'] = raw_data.lon.astype(float)
