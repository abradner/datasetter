from app.settings import Settings
from .dataset import Dataset

settings = Settings()

PRIMARY_KEY = settings.dataset.primary_key

DATASET_FNAME = "listing_locations.sql"

SQL_INTERPOLATIONS = {
    "max_record_count": settings.dataset.max_num_records,
    "data_path": settings.dataset.data_path,
}

class ListingsLocationsDataset(Dataset):
    def __init__(self) -> None:
        super().__init__(DATASET_FNAME, SQL_INTERPOLATIONS)

    def _format_data(self, raw_data):
        # Make sure fields have the right data type
        raw_data['latitude'] = raw_data.latitude.astype(float)
        raw_data['longitude'] = raw_data.longitude.astype(float)
        raw_data['max_travel_distance_meters'] = raw_data.max_travel_distance_meters.astype(float)


    def _validate_data(self, raw_data):
        num_records = len(raw_data)

        # No need for tests if we return a dataset with no rows in it.
        if num_records > 0:

            # Make sure there are no duplicate rows
            unique_key = [PRIMARY_KEY]

            num_unique_records = len(raw_data[unique_key].drop_duplicates())
            if num_records != num_unique_records:
                raise Exception("Some records were duplicates.")


    def _pivot_data(self, raw_data):

        
        data = raw_data # Nothing to do

        return data

