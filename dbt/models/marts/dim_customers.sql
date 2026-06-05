SELECT
    customer_id,
    signup_date,
    country,
    age,
    gender,
    loyalty_tier,
    acquisition_channel

FROM {{ ref('stg_customers') }}