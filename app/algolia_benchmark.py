from typing import List, Tuple
from .algolia_client import Client as AlgoliaClient
from .boundaries_functions import normalise_lat, normalise_lon
from .logger import logger
from .sydney_map import SYDNEY
from .settings import Settings

import Geohash
import os
import pandas as pd
from random import sample
import time
import datetime
import re

settings = Settings()
GEOHASH_PRECISION = settings.geohash_precision


def generate_boundary_filters(lat, lon):
    return [
        "min_lat<" + str(lat),
        "max_lat>" + str(lat),
        "min_lon<" + str(lon),
        "max_lon>" + str(lon),
    ]



def benchmark_searches(client: AlgoliaClient) -> pd.DataFrame:
    df = do_benchmark(client)

    fname = f'{re.sub(":","_", datetime.datetime.now().replace(microsecond=0).isoformat())}.csv'
    df.to_csv(os.path.join(settings.file_system.benchmark_path, fname))
    
    return df

def do_benchmark(client: AlgoliaClient) -> Tuple[List,List,List,List]:
    logger.info("BENCHMARKING")

    boundary_times = []
    boundary_processing_times = []
    boundary_hits = []
    
    geohash_times = []
    geohash_processing_times = []
    geohash_hits = []

    points_list = sample(SYDNEY, len(SYDNEY))

    logger.info("BENCH: WARMING UP")
    for i in range(5):
        start = time.time()
        result = client.query()
        end = time.time()

        runtime = end - start
        logger.info("warmup %i - %2fs" % (i, runtime))


    logger.info("BENCH: BOUNDARY FILTERS")
    for point in points_list:

        lat = normalise_lat(point.lat)
        lon = normalise_lon(point.lon)

        boundary_filters = generate_boundary_filters(lat,lon)

        start = time.time()
        result = client.query(numeric_filters=boundary_filters)
        end = time.time()

        runtime = end - start

        logger.info("point: (%4f,%4f) - %2fs" % (point.lat, point.lon, runtime))

        boundary_times.append(runtime)
        boundary_hits.append(result['nbHits'])
        boundary_processing_times.append(result['processingTimeMS'])


    logger.info("BENCH: GEOHASH FILTERS")
    for point in points_list:

        focal_geohash = Geohash.encode(point.lat, point.lon, GEOHASH_PRECISION)
        filter_string = f'geohashes:{focal_geohash}'

        start = time.time()
        result = client.query(filters=filter_string)
        end = time.time()

        runtime = end - start

        logger.info("point: (%4f,%4f) - %2fs" % (point.lat, point.lon, runtime))

        geohash_times.append(runtime)
        geohash_hits.append(result['nbHits'])
        geohash_processing_times.append(result['processingTimeMS'])


    df = pd.DataFrame(
        {
            "boundary_times": boundary_times,
            "boundary_processing_times": boundary_processing_times,
            "boundary_hits": boundary_hits,

            "geohash_times": geohash_times,
            "geohash_processing_times": geohash_processing_times,
            "geohash_hits": geohash_hits,
        }
    )

    return df

