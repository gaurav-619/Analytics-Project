with customer_cohorts as (

    select

        customer_id,

        date_trunc(signup_date, month) as cohort_month

    from {{ ref('dim_customers') }}

),

customer_activity as (

    select distinct

        customer_id,

        date_trunc(date(timestamp), month) as activity_month

    from {{ ref('fct_transactions') }}

),

cohort_activity as (

    select

        cc.customer_id,

        cc.cohort_month,

        ca.activity_month,

        date_diff(
            ca.activity_month,
            cc.cohort_month,
            month
        ) as cohort_age

    from customer_cohorts cc

    inner join customer_activity ca
        on cc.customer_id = ca.customer_id

),

cohort_size as (

    select

        cohort_month,

        count(distinct customer_id) as cohort_size

    from customer_cohorts

    group by cohort_month

)

select

    ca.cohort_month,

    ca.cohort_age,

    cs.cohort_size,

    count(distinct ca.customer_id) as retained_customers,

    round(
        count(distinct ca.customer_id)
        / cs.cohort_size,
        4
    ) as retention_rate

from cohort_activity ca

left join cohort_size cs
    on ca.cohort_month = cs.cohort_month

group by

    ca.cohort_month,
    ca.cohort_age,
    cs.cohort_size

order by

    ca.cohort_month,
    ca.cohort_age