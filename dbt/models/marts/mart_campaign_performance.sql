WITH transaction_metrics AS (

    SELECT
        campaign_id,

        COUNT(DISTINCT transaction_id) AS total_transactions,

        SUM(net_revenue) AS total_revenue,

        SUM(quantity) AS total_units_sold,

        SUM(
            CASE
                WHEN refund_flag = 1 THEN 1
                ELSE 0
            END
        ) AS total_refunds

    FROM {{ ref('fct_transactions') }}

    WHERE campaign_id IS NOT NULL

    GROUP BY campaign_id

),

event_metrics AS (

    SELECT
        campaign_id,

        COUNT(DISTINCT event_id) AS total_events,

        COUNT(DISTINCT customer_id) AS unique_customers,

        AVG(session_duration_sec) AS avg_session_duration

    FROM {{ ref('fct_events') }}

    WHERE campaign_id IS NOT NULL

    GROUP BY campaign_id

)

SELECT
    c.campaign_id,

    c.channel,
    c.objective,
    c.target_segment,
    c.expected_uplift,

    tm.total_transactions,
    tm.total_revenue,
    tm.total_units_sold,
    tm.total_refunds,

    em.total_events,
    em.unique_customers,
    em.avg_session_duration

FROM {{ ref('dim_campaigns') }} c

LEFT JOIN transaction_metrics tm
    ON c.campaign_id = tm.campaign_id

LEFT JOIN event_metrics em
    ON c.campaign_id = em.campaign_id