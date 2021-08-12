SELECT
    DATE(EVENT_CREATED_UTC_TIMESTAMP) DATE
    , HOUR(EVENT_CREATED_UTC_TIMESTAMP) HOUR
    , LOCATIONS.LATITUDE
    , LOCATIONS.LONGITUDE
    , COUNT(*) NUMBER_OF_EVENTS
FROM {event_source}
    -- To get user default region id
    INNER JOIN {data_path}.USERS
        ON USERS.ID = {event_source}.USER_ID
    -- Get user location
    INNER JOIN {data_path}.USER_LOCATIONS
        ON USER_LOCATIONS.USER_ID = AIRTASKER_EVENT.USER_ID
    -- Get location lat lon
    INNER JOIN {data_path}.LOCATIONS
        ON USER_LOCATIONS.LOCATION_ID = LOCATIONS.ID
WHERE 
    {event_source}.USER_ID IS NOT NULL
    AND EVENT_CREATED_UTC_TIMESTAMP > TIMESTAMPADD(Hour ,-48, current_timestamp())
    AND EVENT_NAME = '{event_name}'
GROUP BY 
    DATE
    , HOUR
    , LATITUDE
    , LONGITUDE

LIMIT {max_record_count}
