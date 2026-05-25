SELECT
    transaction_id,

    CAST(timestamp AS TIMESTAMP) AS timestamp,

    customer_id,

    CAST(product_id AS INT64) AS product_id,

    quantity,
    discount_applied,
    gross_revenue,

    CASE
        WHEN refund_flag = 1 THEN 0
        ELSE gross_revenue
    END AS net_revenue,

    NULLIF(campaign_id, 0) AS campaign_id,

    refund_flag

FROM {{ source('marketing_analytics', 'raw_transactions') }}

WHERE NOT (
    product_id IS NULL
    AND gross_revenue IS NULL
)