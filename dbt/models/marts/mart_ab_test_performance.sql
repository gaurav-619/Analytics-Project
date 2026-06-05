with experiment_events as (

    select

        experiment_group,
        customer_id,
        event_type,
        session_duration_sec

    from {{ ref('fct_events') }}

    where experiment_group is not null

),

experiment_metrics as (

    select

        experiment_group,

        count(distinct customer_id) as total_users,

        count(
            distinct case
                when event_type = 'purchase'
                then customer_id
            end
        ) as purchase_users,

        avg(session_duration_sec) as avg_session_duration_sec,

        count(*) as total_events

    from experiment_events

    group by experiment_group

)

select

    experiment_group,

    total_users,

    purchase_users,

    round(
        purchase_users / total_users,
        4
    ) as conversion_rate,

    round(
        avg_session_duration_sec / 60,
        2
    ) as avg_session_duration_min,

    total_events

from experiment_metrics

order by experiment_group