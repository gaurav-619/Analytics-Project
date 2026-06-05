WITH transaction_metrics AS (

    SELECT
        customer_id,

        COUNT(DISTINCT transaction_id) AS total_transactions,

        SUM(net_revenue) AS total_revenue,

        AVG(net_revenue) AS avg_order_value,

        SUM(quantity) AS total_units_purchased,

        SUM(
            CASE
                WHEN refund_flag = 1 THEN 1
                ELSE 0
            END
        ) AS total_refunds

    FROM {{ ref('fct_transactions') }}

    GROUP BY customer_id

),

event_metrics AS (

    SELECT
        customer_id,

        COUNT(DISTINCT session_id) AS total_sessions,

        COUNT(DISTINCT event_id) AS total_events,

        ROUND(
            AVG(session_duration_sec) / 60,
            2
        ) AS avg_session_duration_min

    FROM {{ ref('fct_events') }}

    GROUP BY customer_id

)

SELECT
    c.customer_id,
    c.country,
    c.age,
    c.gender,
    c.loyalty_tier,
    c.acquisition_channel,

    tm.total_transactions,
    tm.total_revenue,
    tm.avg_order_value,
    tm.total_units_purchased,
    tm.total_refunds,

    em.total_sessions,
    em.total_events,
    em.avg_session_duration_min

FROM {{ ref('dim_customers') }} c

LEFT JOIN transaction_metrics tm
    USING (customer_id)

LEFT JOIN event_metrics em
    USING (customer_id)