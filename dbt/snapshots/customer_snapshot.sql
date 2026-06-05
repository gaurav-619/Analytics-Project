{% snapshot customer_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',

        strategy='check',

        check_cols=[
            'country',
            'age',
            'gender',
            'loyalty_tier',
            'acquisition_channel'
        ]
    )
}}

SELECT *
FROM {{ ref('dim_customers') }}

{% endsnapshot %}