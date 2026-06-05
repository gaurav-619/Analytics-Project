SELECT
    campaign_id,
    channel,
    objective,
    start_date,
    end_date,
    target_segment,
    expected_uplift

FROM {{ ref('stg_campaigns') }}