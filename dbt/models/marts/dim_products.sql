SELECT
    product_id,
    category,
    brand,
    base_price,
    launch_date,
    is_premium

FROM {{ ref('stg_products') }}