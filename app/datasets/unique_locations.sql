SELECT distinct LOCATIONS.latitude as lat, locations.longitude as lon --, locations.display_name
FROM {data_path}.USER_LOCATIONS
    INNER JOIN {data_path}.LOCATIONS
        ON USER_LOCATIONS.location_id = Locations.id
    INNER JOIN {data_path}.USERS
        ON USER_LOCATIONS.user_id = users.id

-- where 1 = 1
    and users.last_activity_at > TIMESTAMPADD(Hour ,-24, current_timestamp())
    and users.last_activity_at < TIMESTAMPADD(Hour ,-20, current_timestamp())

    and users.default_region_id = 1
    and users.last_activity_at is not null

-- order by last_activity_at desc

LIMIT {max_record_count}
