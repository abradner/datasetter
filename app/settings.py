from os import path

from pydantic import BaseModel, BaseSettings

# Create an algolia free account and plug in your details here
class Algolia(BaseModel):
    index = 'location_filtering_benchmark'

    max_records = 9990

# Plug in your snowflake details here
class Snowflake(BaseModel):

class Dataset(BaseModel):
    max_num_records = 200000  # 200 Thousand
    primary_key = 'id'
    main_data_path = 'CHANGE'

class FileSystem(BaseModel):
    file_dir = path.dirname(path.realpath(__file__))
    benchmark_path = path.join(file_dir, 'benchmarks')
    datasets_path = path.join(file_dir, "datasets")
    caches_path = path.join(file_dir, "caches")

class Settings(BaseSettings):
    """
    See https://pydantic-docs.helpmanual.io/#settings for details on using and overriding this
    """

    algolia = Algolia()
    snowflake = Snowflake()
    dataset = Dataset()
    file_system = FileSystem()

    geohash_precision = 5
    