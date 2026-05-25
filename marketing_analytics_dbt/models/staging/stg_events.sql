SELECT
    event_id,
    CAST(timestamp AS TIMESTAMP) AS timestamp,
    customer_id,
    session_id,
    event_type,
    CAST(product_id AS INT64) AS product_id,
    device_type,
    traffic_source,
    NULLIF(campaign_id, 0) AS campaign_id,
    page_category,
    session_duration_sec,
    experiment_group

FROM {{ source('marketing_analytics', 'raw_events') }}