{{
    config(
        materialized="table",
    )
}}
with
    source as (select * from {{ source("oebs", "kostandssteder_kunde") }}),

    payload as (
        select kunde_id, kostnadssted
        from source
        group by all 
    ),

    final as (select * from payload)

select * from final