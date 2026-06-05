
{{
    config(
        materialized='incremental',
        unique_key='event_id'
    )
}}

SELECT
    event_id,
    timestamp,

    customer_id,
    session_id,
    product_id,
    campaign_id,

    event_type,
    device_type,
    traffic_source,
    page_category,

    session_duration_sec,
    experiment_group

FROM {{ ref('stg_events') }}

{% if is_incremental() %}

WHERE timestamp >
(
    SELECT MAX(timestamp)
    FROM {{ this }}
)

{% endif %} 