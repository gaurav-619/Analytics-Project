SELECT
    customer_id,
    CAST(signup_date AS DATE) AS signup_date,
    country,
    age,
    gender,
    loyalty_tier,
    acquisition_channel

FROM {{ source('marketing_analytics', 'raw_customers') }}