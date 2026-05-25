SELECT DISTINCT  
    product_id,
    category,
    brand,
    base_price, 
    launch_date,
    is_premium

FROM {{ source('marketing_analytics', 'raw_products') }}