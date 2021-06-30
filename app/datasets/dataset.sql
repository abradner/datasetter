select listings.id
    , issuer_id
    , title
    , description
    , availability_description
    , value_subunits
    , currency_code
    , category
    , slug
    , welcome_message
    , listings.created_at
    , listings.updated_at
    , latitude
    , longitude
    , max_travel_distance_meters
    , display_name as location_display_name

from "PROD"."RAW_LISTINGS_PUBLIC".LISTINGS as listings

left join prod.raw_listings_public.locations
on locations.id = listings.location_id

where 1=1
    and deleted_at is null
    and purchasable = true
    and location_type = 'in_person'
    and status = 'active'

LIMIT {max_record_count}
