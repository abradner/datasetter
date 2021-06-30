from os import path

from pydantic import BaseModel, BaseSettings

class Algolia(BaseModel):
    app_id = 'CHANGE'
    admin_api_key = 'CHANGE'
    index = 'location_filtering_benchmark'

    max_records = 9990

class Snowflake(BaseModel):
    user='CHANGE'
    password='CHANGE'
    role='CHANGE'
    account='CHANGE'
    warehouse='CHANGE'
    database='CHANGE'

class Dataset(BaseModel):
    max_num_records = 200000  # 200 Thousand
    primary_key = 'id'

class FileSystem(BaseModel):
    file_dir = path.dirname(path.realpath(__file__))
    benchmark_path = path.join(file_dir, 'benchmarks')
    datasets_path = path.join(file_dir, "datasets")
    dataset_sql = path.join(datasets_path, "dataset.sql")

class Settings(BaseSettings):
    """
    See https://pydantic-docs.helpmanual.io/#settings for details on using and overriding this
    """

    algolia = Algolia()
    snowflake = Snowflake()
    dataset = Dataset()
    file_system = FileSystem()

    geohash_precision = 5
    