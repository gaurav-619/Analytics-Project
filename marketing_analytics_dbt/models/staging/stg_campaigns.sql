SELECT
    campaign_id,
    channel,
    objective,
    CAST(start_date AS DATE) AS start_date,
    CAST(end_date AS DATE) AS end_date,
    target_segment,
    expected_uplift
FROM {{ source('marketing_analytics', 'raw_campaigns') }}