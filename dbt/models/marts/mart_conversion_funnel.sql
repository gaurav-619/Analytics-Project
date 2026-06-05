with funnel_stages as (

    select 'view' as event_type, 1 as stage_order
    union all

    select 'click', 2
    union all

    select 'add_to_cart', 3
    union all

    select 'purchase', 4

),

stage_users as (

    select

        fs.stage_order,

        fs.event_type,

        count(distinct fe.customer_id) as users_at_stage

    from {{ ref('fct_events') }} fe

    inner join funnel_stages fs
        on fe.event_type = fs.event_type

    group by

        fs.stage_order,
        fs.event_type

),

funnel_base as (

    select

        users_at_stage as base_users

    from stage_users

    where event_type = 'view'

)

select

    su.stage_order,

    su.event_type,

    su.users_at_stage,

    fb.base_users,

    round(
        su.users_at_stage / fb.base_users,
        4
    ) as overall_conversion_rate,

    round(
        1 - (
            su.users_at_stage / fb.base_users
        ),
        4
    ) as dropoff_rate

from stage_users su

cross join funnel_base fb

order by su.stage_order