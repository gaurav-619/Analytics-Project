SELECT
    p.category,
    p.brand,

    c.country,
    c.loyalty_tier,

    cam.channel,
    cam.objective,

    COUNT(DISTINCT f.transaction_id) AS total_transactions,

    SUM(f.quantity) AS total_units_sold,

    SUM(f.gross_revenue) AS gross_revenue,

    SUM(f.net_revenue) AS net_revenue,

    AVG(f.net_revenue) AS avg_order_value,

    SUM(CASE WHEN f.refund_flag = 1 THEN 1 ELSE 0 END) AS total_refunds

FROM {{ ref('fct_transactions') }} f

LEFT JOIN {{ ref('dim_products') }} p
    ON f.product_id = p.product_id

LEFT JOIN {{ ref('dim_customers') }} c
    ON f.customer_id = c.customer_id

LEFT JOIN {{ ref('dim_campaigns') }} cam
    ON f.campaign_id = cam.campaign_id

GROUP BY
    p.category,
    p.brand,
    c.country,
    c.loyalty_tier,
    cam.channel,
    cam.objective