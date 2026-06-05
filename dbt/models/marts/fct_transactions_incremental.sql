{{ config(
    materialized='incremental',
    unique_key='transaction_id'
) }}

SELECT
    transaction_id,
    timestamp,
    customer_id,
    product_id,
    quantity,
    discount_applied,
    gross_revenue,
    net_revenue,
    campaign_id,
    refund_flag
FROM {{ source('marketing_analytics', 'raw_transactions_incremental') }}

{% if is_incremental() %}

WHERE timestamp >
(
    SELECT MAX(timestamp)
    FROM {{ this }}
)

{% endif %}